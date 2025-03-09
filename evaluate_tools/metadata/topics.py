from bertopic import BERTopic

# Sample documents for topic modeling
docs = [
    "Artificial intelligence and machine learning are revolutionizing the tech industry.",
    "I enjoy reading novels and exploring literature in my free time.",
    "Deep learning models require vast amounts of data for training.",
    "The novel '1984' by George Orwell is a dystopian classic.",
    "Data science combines domain expertise with programming skills.",
    "Literature can offer deep insights into human nature."
]

# Initialize the BERTopic model with default settings
topic_model = BERTopic()

# Fit the model on the documents and obtain topics and their probabilities
topics, probs = topic_model.fit_transform(docs)

# Display overall topic information (topic id, frequency, representative terms, etc.)
print("Topic Information:")
print(topic_model.get_topic_info())

# Optionally, inspect a specific topic (e.g., topic 0)
print("\nDetails of Topic 0:")
print(topic_model.get_topic(0))

# Print out the topic assignment for each document
print("\nDocument Topics:")
for doc, topic in zip(docs, topics):
    print(f"Document: {doc}\nAssigned Topic: {topic}\n")
