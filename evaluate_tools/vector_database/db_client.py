"""
SermonVectorDB: A class-based interface for managing sermon data in Weaviate.
Supports schema initialization, CRUD operations, and semantic search.
"""

import weaviate
from weaviate.collections.classes.config import (
    Property,
    DataType,
    InvertedIndexConfig,
    MultiTenancyConfig,
    ReplicationConfig,
)
from weaviate.exceptions import WeaviateBaseError


class SermonVectorDB:
    """
    Class-based interface for managing sermon data in Weaviate.
    Supports schema initialization, CRUD operations, and semantic search.
    """
    def __init__(self, url="http://localhost:8080"):
        self.client = weaviate.WeaviateClient(url)
        self.collection_name = "Sermon"
        self._init_schema()

    def _init_schema(self):
        """Initialize the Sermon schema if not present."""
        try:
            collections = self.client.collections.list_all()
            if self.collection_name not in collections:
                self.client.collections.create(
                    name=self.collection_name,
                    description="A collection of sermon texts for vector search",
                    generative_config=None,
                    inverted_index_config=InvertedIndexConfig(
                        bm25=None,
                        cleanup_interval_seconds=60,
                        index_null_state=True,
                        index_property_length=True,
                        index_timestamps=True,
                        stopwords=None
                    ),
                    multi_tenancy_config=MultiTenancyConfig(
                        enabled=False,
                        auto_tenant_creation=False,
                        auto_tenant_activation=False
                    ),
                    properties=[
                        Property(name="title", data_type=DataType.TEXT),
                        Property(name="content", data_type=DataType.TEXT),
                    ],
                    references=[],
                    replication_config=ReplicationConfig(
                        factor=1,
                        async_enabled=False,
                        deletion_strategy="DeleteOnConflict"
                    ),
                    reranker_config=None,
                    sharding_config=None,
                    vector_index_config=None,
                    vectorizer_config="text2vec-transformers"
                )
                print("Schema created successfully.")
            else:
                print("Schema already exists.")
        except WeaviateBaseError as e:
            print(f"Schema initialization error: {e}")

    def add_sermon(self, title, content, metadata=None):
        """Add a new sermon with title, content, and optional metadata."""
        data = {"title": title, "content": content}
        if metadata:
            data.update(metadata)
        try:
            collection = self.client.collections.get(self.collection_name)
            collection.data.insert(data)
            print(f"Sermon '{title}' added.")
        except WeaviateBaseError as e:
            print(f"Error adding sermon: {e}")

    def search_sermons(self, concepts, limit=5):
        """Search sermons by concepts/keywords using nearText."""
        try:
            collection = self.client.collections.get(self.collection_name)
            results = collection.query.near_text(
                query=concepts,
                limit=limit,
                return_properties=["title", "content"]
            )
            return results.objects
        except WeaviateBaseError as e:
            print(f"Search error: {e}")
            return []

    def update_sermon(self, uuid, updates):
        """Update a sermon entry by UUID."""
        try:
            collection = self.client.collections.get(self.collection_name)
            collection.data.update(uuid, updates)
            print(f"Sermon {uuid} updated.")
        except WeaviateBaseError as e:
            print(f"Update error: {e}")

    def delete_sermon(self, uuid):
        """Delete a sermon entry by UUID."""
        try:
            collection = self.client.collections.get(self.collection_name)
            collection.data.delete(uuid)
            print(f"Sermon {uuid} deleted.")
        except WeaviateBaseError as e:
            print(f"Delete error: {e}")

# Example usage:
# db = SermonVectorDB()
# db.add_sermon("Faith and Hope", "This sermon explores the deep connection between faith and hope.")
# results = db.search_sermons(["faith", "hope"])
# print(results)
