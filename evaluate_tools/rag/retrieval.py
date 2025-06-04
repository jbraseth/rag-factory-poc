"""
Retrieval utilities for querying sermon passages using LlamaIndex ≥ 0.9
"""

import os
import json
from llama_index.core import Document, VectorStoreIndex

class SermonVectorDB:
    """
    Vector database for sermon transcripts and metadata using LlamaIndex.
    Loads transcripts and metadata from the pipeline data directories.
    """

    def __init__(self, transcripts_dir=None, metadata_dir=None):
        """
        Initialize the vector database, loading documents from the specified directories.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.transcripts_dir = transcripts_dir or os.path.join(base_dir, "data", "transcripts")
        self.metadata_dir = metadata_dir or os.path.join(base_dir, "data", "sermons")
        self.documents = []
        self._load_documents()
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine()

    def _load_documents(self):
        """
        Load all transcript and metadata files into Document objects.
        """
        for fname in os.listdir(self.transcripts_dir):
            if fname.endswith(".txt"):
                transcript_path = os.path.join(self.transcripts_dir, fname)
                base = os.path.splitext(fname)[0]
                metadata_path = os.path.join(self.metadata_dir, f"{base}.json")
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read()
                metadata = {}
                if os.path.exists(metadata_path):
                    with open(metadata_path, "r", encoding="utf-8") as mf:
                        metadata = json.load(mf)
                else:
                    metadata = {"title": base, "speaker": "Unknown", "timestamp": "Unknown"}
                self.documents.append(Document(text=text, metadata=metadata))

    def add_sermon(self, title, text, metadata=None):
        """
        Add a new sermon to the database and update the index.
        """
        meta = metadata or {"title": title}
        self.documents.append(Document(text=text, metadata=meta))
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine()

    def search_sermons(self, queries):
        """
        Search for relevant sermon passages given a query or list of queries.
        Returns a list of dicts with text, metadata, and score.
        """
        if isinstance(queries, str):
            queries = [queries]
        results = []
        for query in queries:
            response = self.query_engine.query(query)
            for node in getattr(response, "source_nodes", []):
                results.append({
                    "text": node.node.get_content(),
                    "metadata": node.node.metadata or {},
                    "score": node.score,
                })
            if not getattr(response, "source_nodes", []):
                results.append({"text": response.response, "metadata": {}})
        return results

# Example usage:
# db = SermonVectorDB()
# db.add_sermon("Faith and Hope", "This sermon explores the deep connection between faith and hope.")
# results = db.search_sermons(["faith", "hope"])
# print(results)
