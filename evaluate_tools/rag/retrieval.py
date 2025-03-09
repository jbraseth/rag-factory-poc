from llama_index import Document, GPTSimpleVectorIndex

# Define sample sermon documents with metadata
documents = [
    Document(
        text="This sermon discusses the power of forgiveness and redemption. It reminds us that mercy is a divine gift.",
        metadata={"title": "Forgiveness and Redemption", "speaker": "Pastor Mark", "timestamp": "2023-02-10"}
    ),
    Document(
        text="In this message, we explore faith, hope, and love. The sermon emphasizes trusting in divine guidance.",
        metadata={"title": "Faith, Hope, and Love", "speaker": "Pastor John", "timestamp": "2023-01-15"}
    ),
    Document(
        text="This sermon focuses on community unity and support during times of adversity. It highlights the strength in togetherness.",
        metadata={"title": "Community Unity", "speaker": "Pastor Luke", "timestamp": "2023-03-05"}
    )
]

# Build the vector index using GPTSimpleVectorIndex
index = GPTSimpleVectorIndex(documents)

# Query the index for relevant sermon passages
query = "What does the sermon say about forgiveness?"
response = index.query(query)

print("Query:", query)
print("Response:", response)
