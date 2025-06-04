"""Tests for SermonVectorDB retrieval using LlamaIndex."""

import json

import pytest

from evaluate_tools.rag.retrieval import SermonVectorDB


@pytest.mark.description("SermonVectorDB should initialize with correct directories")
def test_search_sermons_returns_expected_fields(tmp_path):
    # Setup: create dummy transcript and metadata files
    transcripts_dir = tmp_path / "transcripts"
    metadata_dir = tmp_path / "sermons"
    transcripts_dir.mkdir()
    metadata_dir.mkdir()
    transcript_path = transcripts_dir / "sermon1.txt"
    metadata_path = metadata_dir / "sermon1.json"
    transcript_text = "Blessed are the peacemakers."
    metadata = {"title": "Sermon on the Mount", "speaker": "Jesus", "timestamp": "AD 30"}
    transcript_path.write_text(transcript_text, encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

    # Create DB and search
    db = SermonVectorDB(transcripts_dir=str(transcripts_dir), metadata_dir=str(metadata_dir))
    results = db.search_sermons("peacemakers")

    assert isinstance(results, list)
    assert results
    assert "text" in results[0]
    assert "metadata" in results[0]
    assert transcript_text in results[0]["text"]
    assert results[0]["metadata"]["title"] == "Sermon on the Mount"
