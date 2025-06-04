"""Tests for scripture reference extraction."""

import pytest

from evaluate_tools.metadata.references import extract_scripture_references


@pytest.fixture(autouse=True)
def mock_spacy(monkeypatch):
    """Mock spaCy NLP and NER for reference extraction."""
    class MockDoc:
        ents = []
    def fake_nlp(text):
        _ = text  # ignore the text
        return MockDoc()
    monkeypatch.setattr("evaluate_tools.metadata.references.nlp", fake_nlp)


@pytest.mark.description("regex-only scripture should extract reference")
def test_extract_scripture_references_regex_only():
    text = "Today we read from John 3:16 and 1 Corinthians 13:4-7."
    refs = extract_scripture_references(text)
    assert "John 3:16" in refs
    assert any("Corinthians 13:4-7" in r for r in refs)


@pytest.mark.description("extraction should return empty list for empty input")
def test_extract_scripture_references_empty():
    refs = extract_scripture_references("")
    assert refs == []
