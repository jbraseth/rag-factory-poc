"""Tests for audio transcription utilities."""

import pytest

from evaluate_tools.transcription.transcribe import transcribe_audio


class DummyClient:
    """Dummy OpenAI client for mocking."""
    class Audio:
        class Transcriptions:
            def create(self, file, model, response_format, timestamp_granularities):
                _, _, _, _ = file, model, response_format, timestamp_granularities  # ignore the arguments
                class Result:
                    words = [type("Word", (), {"word": "hello", "start": 0.0, "end": 0.2})()]
                return Result()
        transcriptions = Transcriptions()
    audio = Audio()


def dummy_openai(*args, **kwargs):
    _, _ = args, kwargs  # unused but needed for method signature
    return DummyClient()


@pytest.fixture(name="patch_openai")
def fixture_patch_openai(monkeypatch):
    """Patch OpenAI with dummy client."""
    monkeypatch.setattr("evaluate_tools.transcription.transcribe.OpenAI", dummy_openai)


@pytest.mark.description("transcribe_audio should return expected text and words")
def test_transcribe_audio_openai(patch_openai, tmp_path):
    _ = patch_openai  # unused but needed for fixture
    path = tmp_path / "file.mp3"
    path.write_bytes(b"123")
    text, words = transcribe_audio(str(path), use_whisper_cpp=False)
    assert text == "hello"
    assert isinstance(words, list)
    assert words[0]["word"] == "hello"
