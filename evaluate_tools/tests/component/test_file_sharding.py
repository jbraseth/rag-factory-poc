"""Tests for audio file sharding utilities."""

import os

import pytest

from evaluate_tools.transcription.file_sharding import split_audio


class DummyAudioSegment:
    """Dummy audio segment for mocking pydub.AudioSegment."""
    def __init__(self, duration_ms=30000):
        self.duration = duration_ms

    def __len__(self):
        return self.duration

    def __getitem__(self, idx):
        return self

    def export(
            self,
            out_file,
            format
        ):  # pylint: disable=redefined-builtin
        _ = format  # ignore the format
        with open(out_file, "wb"):
            return b"dummy audio data"


@pytest.fixture(name="mock_audio_segment")
def fixture_mock_audio_segment(monkeypatch, tmp_path):
    """Mock AudioSegment.from_mp3 and path functions."""
    _ = tmp_path # not used but needed to create a temporary directory
    monkeypatch.setattr("pydub.AudioSegment.from_mp3", lambda f: DummyAudioSegment(60000))
    monkeypatch.setattr("os.path.splitext", lambda f: ("test", ".mp3"))
    monkeypatch.setattr("os.path.basename", lambda f: "test.mp3")


@pytest.mark.description("split_audio should return correct chunk files")
def test_split_audio(
        mock_audio_segment, tmp_path
    ):
    _, _ = mock_audio_segment, tmp_path  # unused but needed for fixture
    files = split_audio("dummy.mp3", chunk_length_minutes=1)
    assert len(files) == 1
    assert files[0].endswith(".mp3")
    assert os.path.exists(files[0])
