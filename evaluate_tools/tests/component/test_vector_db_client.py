"""Tests for SermonVectorDB Weaviate client."""

import pytest

from evaluate_tools.vector_database.db_client import SermonVectorDB


class DummyWeaviateClient:
    """Dummy Weaviate client for mocking."""
    class Collections:
        def list_all(self):
            return []
        def create(self, **kwargs):
            _ = kwargs  # ignore the arguments
        def get(self, name):
            _ = name  # ignore the name
            return self
        class Data:
            def insert(self, data):
                _ = data  # ignore the data
            def update(self, uuid, updates):
                _ = uuid, updates  # ignore the arguments
            def delete(self, uuid):
                _ = uuid  # ignore the uuid
        data = Data()
        class Query:
            def near_text(self, query, limit, return_properties):
                _, _, _ = query, limit, return_properties  # ignore the arguments
                return type("R", (), {"objects": [{"title": "foo", "content": "bar"}]})()
        query = Query()
    collections = Collections()


@pytest.fixture(name="patch_weaviate")
def fixture_patch_weaviate(monkeypatch):
    """Patch WeaviateClient and config classes with dummies."""
    monkeypatch.setattr("weaviate.WeaviateClient", lambda url: DummyWeaviateClient())
    monkeypatch.setattr("weaviate.collections.classes.config.Property", lambda **k: None)
    monkeypatch.setattr("weaviate.collections.classes.config.DataType", type("DataType", (), {"TEXT": "text"}))
    monkeypatch.setattr("weaviate.collections.classes.config.InvertedIndexConfig", lambda **k: None)
    monkeypatch.setattr("weaviate.collections.classes.config.MultiTenancyConfig", lambda **k: None)
    monkeypatch.setattr("weaviate.collections.classes.config.ReplicationConfig", lambda **k: None)
    monkeypatch.setattr("weaviate.exceptions.WeaviateBaseError", Exception)


@pytest.mark.description("SermonVectorDB should initialize Weaviate client correctly")
def test_db_add_and_search(patch_weaviate):
    _ = patch_weaviate  # unused but needed for fixture
    db = SermonVectorDB()
    db.add_sermon("Title", "Content")
    results = db.search_sermons(["foo"])
    assert isinstance(results, list)
    assert results[0]["title"] == "foo"
