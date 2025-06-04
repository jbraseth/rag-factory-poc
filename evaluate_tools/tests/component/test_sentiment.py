"""Tests for sentiment and emotion analysis."""

import pytest

from evaluate_tools.metadata import sentiment


@pytest.fixture(name="mock_emotion_analyzer")
def fixture_mock_emotion_analyzer(monkeypatch):
    """Mock emotion_analyzer pipeline."""
    def fake_pipeline(text):
        _ = text  # ignore the text
        return [[{"label": "joy", "score": 0.95}, {"label": "sadness", "score": 0.05}]]
    monkeypatch.setattr("evaluate_tools.metadata.sentiment.emotion_analyzer", fake_pipeline)


@pytest.mark.description("analyze_sentiment should return dominant emotion and scores")
def test_analyze_sentiment_basic(mock_emotion_analyzer):
    _ = mock_emotion_analyzer  # unused but needed for fixture
    label, scores = sentiment.analyze_sentiment("test")
    assert label == "joy"
    assert isinstance(scores, list)
    assert any("label" in s for s in scores)
