"""
Speaker diarization utilities for segmenting audio by speaker and aligning transcript text.
"""

import numpy as np
import librosa
from speechbrain.processing.diarization import Spec_Clust_unorm


def extract_embeddings(audio, sr, chunk_duration=2.0, rng=None, seed=None):
    """
    Dummy placeholder for extracting speaker embeddings from audio.
    In the actual pipeline, you would load your model and extract embeddings for each chunk.
    Replace this function with your own embedding extractor.
    """
    if rng is None:
        rng = np.random.default_rng(seed)
    n_chunks = int(np.ceil(len(audio) / (chunk_duration * sr)))
    return rng.random((n_chunks, 192))  # 192-dim is typical for ECAPA embeddings

def diarize_speakers(audio_file, transcript=None, chunk_duration=2.0, n_speakers=2, seed=None):
    """
    Segments audio into speaker-labeled chunks and optionally aligns transcript text.

    Args:
        audio_file (str): Path to the audio file.
        transcript (str, optional): Transcript to align with segments.
        chunk_duration (float): Duration (seconds) of each chunk.
        n_speakers (int): Number of speakers to cluster.
        seed (int, optional): Random seed for reproducibility.

    Returns:
        List[dict]: List of segments with start, end, speaker, and optional text.
    """
    audio, sr = librosa.load(audio_file, sr=16000)
    chunk_len = int(chunk_duration * sr)
    chunk_times = [
        (s / sr, min((s + chunk_len), len(audio)) / sr)
        for s in np.arange(0, len(audio), chunk_len)
    ]

    rng = np.random.default_rng(seed)
    embeddings = extract_embeddings(audio, sr, chunk_duration, rng=rng)
    clust = Spec_Clust_unorm(min_num_spkrs=2, max_num_spkrs=10)
    clust.do_spec_clust(embeddings, k_oracle=n_speakers, p_val=0.3)
    labels = clust.labels_

    segments = [
        {
            "start": float(start),
            "end": float(end),
            "speaker": f"spk{label+1}"
        }
        for (start, end), label in zip(chunk_times, labels)
    ]

    if transcript and isinstance(transcript, str) and segments:
        words = transcript.split()
        words_per_segment = max(1, len(words) // len(segments))
        for idx, seg in enumerate(segments):
            start_idx = idx * words_per_segment
            end_idx = (idx + 1) * words_per_segment if idx < len(segments) - 1 else len(words)
            seg["text"] = " ".join(words[start_idx:end_idx])

    return segments

# Example:
# segments = diarize_speakers("audio.wav", transcript="optional transcript here", seed=42)
# print(segments)
