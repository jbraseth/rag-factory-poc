from transformers import pipeline

# Initialize the pipeline with the emotion model
model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_analyzer = pipeline("text-classification", model=model_name, return_all_scores=True)

# Sample sermon-like text snippets
sermon_texts = [
    "Today we reflect on the blessings we have received, and the gratitude in our hearts.",
    "We should be mindful of our sins and seek forgiveness with humility.",
    "There is a powerful joy in knowing that God is with us in our struggles."
]

# Analyze each snippet
for text in sermon_texts:
    scores = emotion_analyzer(text)
    print(f"Text: {text}")
    print("Emotion Scores:", scores)
    print("--------------")
