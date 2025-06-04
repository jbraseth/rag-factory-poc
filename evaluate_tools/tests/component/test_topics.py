"""Tests for topic extraction using BERTopic."""

import pytest

from evaluate_tools.metadata.topics import extract_topics


class MockBERTopic:
    """Mock BERTopic class for testing."""
    def fit_transform(self, docs):
        _ = docs  # ignore the documents
        return [0], None
    def get_topic(self, topic_id):
        _ = topic_id  # ignore the topic ID
        return [("forgiveness", 0.5), ("love", 0.3)]


@pytest.fixture(name="mock_bertopic")
def fixture_mock_bertopic(monkeypatch):
    """Mock BERTopic with a simple implementation."""
    def fake_bertopic():
        return MockBERTopic()
    monkeypatch.setattr("evaluate_tools.metadata.topics.BERTopic", fake_bertopic)


@pytest.mark.description("extract_topics should return expected topics")
def test_extract_topics(mock_bertopic):
    _ = mock_bertopic  # unused but needed for fixture
    topics = extract_topics("This is a test sermon about forgiveness and love.")
    assert "forgiveness" in topics
    assert "love" in topics
