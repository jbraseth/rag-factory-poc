"""
Topic extraction from sermon transcripts using BERTopic.
"""

from collections import Counter
from itertools import tee
from typing import List, Tuple, Optional

import re
import spacy
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from umap import UMAP
from bertopic import BERTopic

# Ensure NLTK data is present
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Initialize spaCy (no NER, no parser for speed)
_nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Stop-word lists
_stop_basic = set(nltk.corpus.stopwords.words("english"))
_stop_extra = {
    "m","s","t","im","youre","dont","like","know","just","let"
}


def _clean_and_filter(text: str) -> List[str]:
    """Lowercase, remove punct, stop-words, keep only NOUN/ADJ lemmas."""
    tokens = re.sub(r"[^\w\s]", " ", text.lower()).split()
    tokens = [
        w for w in tokens
        if w not in _stop_basic and w not in _stop_extra and len(w) > 2
    ]
    doc = _nlp(" ".join(tokens))
    return [tok.lemma_ for tok in doc if tok.pos_ in {"NOUN", "ADJ"}]


def _add_bigrams(tokens: List[str], min_count: int = 2) -> List[str]:
    """
    Pure-Python bigram merger.
    Keeps only those bigrams that occur >= min_count times within this token list.
    """
    t1, t2 = tee(tokens)
    next(t2, None)
    bigrams = ["_".join(pair) for pair in zip(t1, t2)]
    freq = Counter(bigrams)
    return tokens + [bg for bg in bigrams if freq[bg] >= min_count]


def extract_topics(
    transcripts: List[str],
    n_topics: int = 3,
    min_df: int = 2,
    bigram_min_count: int = 2,
    umap_n_neighbors: int = 5,
    umap_n_components: int = 2,
) -> List[Optional[List[Tuple[str, float]]]]:
    """
    Runs topic modeling over a list of chunk transcripts.
    
    Args:
      transcripts: List of raw transcript strings (one per chunk).
      n_topics:    How many sub-topics (K) to force via KMeans.
      min_df:      min document frequency for CountVectorizer.
      bigram_min_count: minimum times a bigram must appear within a chunk.
      umap_n_neighbors, umap_n_components: UMAP settings.
    
    Returns:
      A list (same length as transcripts) of topic lists, where each topic list
      is List[(term, score)].  If BERTopic returns None for a chunk, we return None.
    """
    # 1) Preprocess each chunk
    token_chunks = [_clean_and_filter(t) for t in transcripts]
    token_chunks = [_add_bigrams(tc, min_count=bigram_min_count) for tc in token_chunks]
    docs = [" ".join(toks) for toks in token_chunks]

    # 2) Configure BERTopic with KMeans and UMAP
    vectorizer = CountVectorizer(min_df=min_df, ngram_range=(1, 2))
    umap_model  = UMAP(
        n_neighbors=umap_n_neighbors,
        n_components=umap_n_components,
        init="random",
        metric="cosine"
    )
    kmeans = KMeans(n_clusters=n_topics, random_state=42)

    topic_model = BERTopic(
        hdbscan_model     = kmeans,
        umap_model        = umap_model,
        vectorizer_model  = vectorizer,
        calculate_probabilities = False,
        verbose = False
    )

    # 3) Fit & transform
    topics, _ = topic_model.fit_transform(docs)

    # 4) Gather resulting term-score lists
    out: List[Optional[List[Tuple[str, float]]]] = []
    for t in topics:
        info = topic_model.get_topic(t)
        out.append(info if info is not None else None)

    return out

# Example usage:
# transcript = (
#     "Artificial intelligence and machine learning are revolutionizing the tech industry. "
#     "Deep learning models require vast amounts of data for training. "
#     "Data science combines domain expertise with programming skills."
# )
# print(extract_topics(transcript))
