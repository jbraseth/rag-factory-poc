"""
Module for transcribing audio files using either whisper.cpp or the OpenAI Whisper API.
Provides a function to transcribe audio and extract word-level timestamps.
"""

import os
import subprocess
import json
from openai import OpenAI


def transcribe_audio(file_path, use_whisper_cpp=False, whisper_cpp_path="whisper.cpp/main", model_path="models/ggml-base.en.bin", openai_api_key=None):
    """
    Transcribes an audio file using whisper.cpp if available, otherwise falls back to OpenAI Whisper API.
    Returns:
        transcript_text (str): The full transcript as a string.
        word_timestamps (list): List of dicts with word and timestamp info (if available).
    """
    transcript_text = ""
    word_timestamps = []

    if use_whisper_cpp and os.path.exists(whisper_cpp_path):
        # Use whisper.cpp via subprocess
        output_json = "transcript.json"
        cmd = [
            whisper_cpp_path,
            "-m", model_path,
            "-f", file_path,
            "-otxt",
            "-of", "transcript",
            "-oj"
        ]
        subprocess.run(cmd, check=True)
        # Read the output JSON
        if os.path.exists(output_json):
            with open(output_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            segments = data.get("segments", [])
            transcript_text = " ".join(seg["text"] for seg in segments)
            for seg in segments:
                for word in seg.get("words", []):
                    word_timestamps.append({
                        "word": word["word"],
                        "start": word["start"],
                        "end": word["end"]
                    })
        else:
            raise RuntimeError("whisper.cpp did not produce transcript.json")
    else:
        # Use OpenAI Whisper API
        client = OpenAI(api_key=openai_api_key) if openai_api_key else OpenAI()
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
            transcript_text = " ".join([w.word for w in transcription.words])
            word_timestamps = [
                {"word": w.word, "start": w.start, "end": w.end}
                for w in transcription.words
            ]

    return transcript_text, word_timestamps

# Example usage:
# text, words = transcribe_audio("good_morning.mp3", use_whisper_cpp=True)
