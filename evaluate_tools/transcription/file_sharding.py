"""
Module for splitting audio files into smaller chunks using pydub.
"""

import os
from pydub import AudioSegment


def split_audio(file_path, chunk_length_minutes=10):
    """
    Splits an audio file into chunks of specified length (in minutes).
    Returns a list of file paths for each chunk.
    """
    audio = AudioSegment.from_mp3(file_path)
    chunk_length_ms = chunk_length_minutes * 60 * 1000
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    base, ext = os.path.splitext(os.path.basename(file_path))
    output_files = []
    for idx, chunk in enumerate(chunks):
        out_file = f"{base}_chunk_{idx}{ext}"
        chunk.export(out_file, format="mp3")
        output_files.append(out_file)
    return output_files

# Example usage:
# chunk_files = split_audio("good_morning.mp3", 10)
