from types import SimpleNamespace

import pytest

from main import main


@pytest.fixture
def capture_print(monkeypatch):
    printed = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: printed.append(a[0] if a else ""))
    return printed


@pytest.fixture
def base_dependencies(monkeypatch):
    """Patch all main dependencies with default (single chunk) behavior."""
    mock_db = SimpleNamespace()
    mock_db.data_object = SimpleNamespace(create=lambda *a, **k: None)
    mock_db_client = SimpleNamespace(client=mock_db)
    mock_vector_db = SimpleNamespace(search_sermons=lambda q: [{"text": "retrieved text", "metadata": {"title": "Sermon Title"}}])
    mock_analyze_sermon_action = lambda *a, **k: "GPT response"
    mock_emotion_analyzer = lambda *a, **k: {"sentiment": "positive"}
    mock_spacy_doc = SimpleNamespace(ents=[SimpleNamespace(text="John", label_="PERSON")])
    mock_spacy_nlp = lambda *a, **k: mock_spacy_doc
    mock_diarize_speakers = lambda *a, **k: {"speaker": "A"}
    mock_transcribe_audio = lambda *a, **k: ("transcript text", None)
    mock_split_audio = lambda *a, **k: ["chunk1.wav"]

    monkeypatch.setattr("main.db_client", mock_db_client)
    monkeypatch.setattr("main.SermonVectorDB", lambda: mock_vector_db)
    monkeypatch.setattr("main.analyze_sermon_action", mock_analyze_sermon_action)
    monkeypatch.setattr("main.emotion_analyzer", mock_emotion_analyzer)
    monkeypatch.setattr("main.spacy_nlp", mock_spacy_nlp)
    monkeypatch.setattr("main.diarize_speakers", mock_diarize_speakers)
    monkeypatch.setattr("main.transcribe_audio", mock_transcribe_audio)
    monkeypatch.setattr("main.split_audio", mock_split_audio)


@pytest.fixture
def single_chunk_no_bertopic(base_dependencies, monkeypatch):
    called = {}
    monkeypatch.setattr("main.BERTopic", lambda *a, **k: called.setdefault("called", True))
    # Patch analyze_sermon_action to capture metadata
    metadata_holder = {}
    def fake_analyze_sermon_action(query, retrieved, metadata):
        metadata_holder["metadata"] = metadata
        return "GPT response"
    monkeypatch.setattr("main.analyze_sermon_action", fake_analyze_sermon_action)
    called["metadata_holder"] = metadata_holder
    return called


@pytest.fixture
def multi_chunk_with_bertopic(base_dependencies, monkeypatch):
    """Patch BERTopic to track calls, and split_audio to return two chunks."""
    called = {}
    class DummyTopicModel:
        def fit_transform(self, docs):
            called["fit_transform"] = docs
            return ([0, 1], None)
        def get_topic(self, idx):
            return [[("topic1", 0.5)], [("topic2", 0.7)]][idx]
    monkeypatch.setattr("main.BERTopic", lambda *a, **k: DummyTopicModel())
    # Patch split_audio to return two chunks
    monkeypatch.setattr("main.split_audio", lambda *a, **k: ["chunk1.wav", "chunk2.wav"])
    # Patch transcribe_audio to return different texts
    monkeypatch.setattr("main.transcribe_audio", lambda *a, **k: ("text1", None) if a[0] == "chunk1.wav" else ("text2", None))
    # Patch spacy_nlp to return different docs
    doc1 = SimpleNamespace(ents=[SimpleNamespace(text="Alice", label_="PERSON")])
    doc2 = SimpleNamespace(ents=[SimpleNamespace(text="Bob", label_="PERSON")])
    docs = iter([doc1, doc2])
    monkeypatch.setattr("main.spacy_nlp", lambda *a, **k: next(docs))
    # Patch diarize_speakers to return different speakers
    monkeypatch.setattr("main.diarize_speakers", lambda *a, **k: {"speaker": "A"} if a[0] == "chunk1.wav" else {"speaker": "B"})
    # Patch emotion_analyzer to return different sentiments
    monkeypatch.setattr("main.emotion_analyzer", lambda *a, **k: {"sentiment": "happy"} if a[0] == "text1" else {"sentiment": "sad"})
    return called


@pytest.mark.description("main() with a single chunk does NOT call BERTopic and returns fallback topic info")
def test_main_single_chunk_no_topic_model(single_chunk_no_bertopic, capture_print):
    main("audio.mp3", "query")
    assert "called" not in single_chunk_no_bertopic
    assert "Final RAG Pipeline Response:" in capture_print
    assert "GPT response" in capture_print


@pytest.mark.description("main() with multiple chunks DOES call BERTopic and assigns topics")
def test_main_multiple_chunks_calls_topic_model(multi_chunk_with_bertopic, capture_print):
    main("audio.mp3", "query")
    # BERTopic should be called and fit_transform called with both chunks
    assert "fit_transform" in multi_chunk_with_bertopic
    assert multi_chunk_with_bertopic["fit_transform"] == ["text1", "text2"]
    assert "Final RAG Pipeline Response:" in capture_print
    assert "GPT response" in capture_print
