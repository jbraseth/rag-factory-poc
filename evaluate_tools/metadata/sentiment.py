"""
Sentiment and emotion analysis for sermon transcripts using a transformer model.
"""

from transformers import pipeline

# Truncate any input over 512 tokens so we never exceed the model's max length
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
emo_pipe = pipeline(
    "text-classification",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
    return_all_scores=True,
    truncation=True,
    max_length=512,
)

def analyze_sentiment(transcript: str):
    """
    1) Split transcript into ~450-word chunks
    2) Run emo_pipe on each chunk to get all label scores
    3) Average each emotion’s score across chunks
    4) Return (dominant_label, [ {label, score}, … ])
    """
    words = transcript.split()
    window = 450
    chunks = [" ".join(words[i : i + window]) for i in range(0, len(words), window)]

    # collect per-chunk dicts: { "joy":0.12, "sadness":0.05, … }
    chunk_scores = []
    for chunk in chunks:
        scores = emo_pipe(chunk)[0]   # list of dicts
        chunk_scores.append({d["label"]: d["score"] for d in scores})

    # average across chunks
    labels = chunk_scores[0].keys()
    avg_scores = {
        label: sum(d[label] for d in chunk_scores) / len(chunk_scores)
        for label in labels
    }

    # pick the top
    dominant = max(avg_scores, key=lambda k: avg_scores[k])

    # repackage as list of dicts
    final_scores = [{"label": l, "score": avg_scores[l]} for l in avg_scores]

    return dominant, final_scores

# Example usage:
# transcript = "Today we reflect on the blessings we have received, and the gratitude in our hearts."
# label, scores = analyze_sentiment(transcript)
# print(f"Dominant Emotion: {label}")
# print("All Scores:", scores)
