"""Tests for speaker diarization utilities."""

import numpy as np
import pytest

from evaluate_tools.transcription.diarization import diarize_speakers


@pytest.fixture(name="mock_librosa")
def fixture_mock_librosa(monkeypatch):
    """Mock librosa.load to return dummy audio."""
    monkeypatch.setattr("librosa.load", lambda *args, **kwargs: (np.ones(16000*10), 16000))


@pytest.fixture(name="mock_spec_clust")
def fixture_mock_spec_clust(monkeypatch):
    """Mock Spec_Clust_unorm to return dummy labels."""
    class DummyClust:
        labels_ = [0, 1, 0, 1, 0]
        def do_spec_clust(self, *args, **kwargs):
            _, _ = args, kwargs  # unused but needed for method signature
    monkeypatch.setattr("speechbrain.processing.diarization.Spec_Clust_unorm", lambda *a, **k: DummyClust())


@pytest.mark.description("diarize_speakers should return segments with expected fields")
def test_diarize_speakers(mock_librosa, mock_spec_clust):
    _, _ = mock_librosa, mock_spec_clust  # unused but needed for fixture
    segments = diarize_speakers(
        "dummy.wav",
        transcript="one two three four five six seven eight nine ten",
        n_speakers=2
    )
    assert all("speaker" in seg for seg in segments)
    assert all("start" in seg and "end" in seg for seg in segments)
    assert segments[0]["speaker"].startswith("spk")
    assert all("text" in seg for seg in segments)
