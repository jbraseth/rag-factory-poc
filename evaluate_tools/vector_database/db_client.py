import weaviate

# Initialize the Weaviate client to connect to the local instance
client = weaviate.Client("http://localhost:8080")

# Check if Weaviate is live
if client.is_live():
    print("Weaviate is live!")
else:
    print("Weaviate is not live. Please check your setup.")

# Define a simple schema for a 'Sermon' class
schema = {
    "classes": [
        {
            "class": "Sermon",
            "description": "A collection of sermon texts for vector search",
            "vectorizer": "text2vec-transformers",  # Ensure this module is enabled in your docker-compose.yml
            "properties": [
                {
                    "name": "title",
                    "dataType": ["text"]
                },
                {
                    "name": "content",
                    "dataType": ["text"]
                }
            ]
        }
    ]
}

# Create the schema in Weaviate
client.schema.create(schema)
print("Schema created successfully.")

# Add a sample sermon object
sermon_object = {
    "title": "Faith and Hope",
    "content": "This sermon explores the deep connection between faith and hope, highlighting that through belief we find strength."
}

client.data_object.create(sermon_object, "Sermon")
print("Sample sermon object added.")

# Perform a query using nearText search
query = """
{
  Get {
    Sermon(nearText: {
      concepts: ["faith", "hope"]
    }) {
      title
      content
    }
  }
}
"""

result = client.query.raw(query)
print("Query result:", result)
