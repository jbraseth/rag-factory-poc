"""
Custom GPT actions for sermon analysis and metadata enrichment.
"""

import re


def generate_embed_link(title: str) -> str:
    """
    Generate an embed link based on the sermon title.
    For example, "Forgiveness and Redemption" becomes:
    https://sermons.example.com/embed/forgiveness-and-redemption
    """
    slug = re.sub(r'\W+', '-', title.lower()).strip('-')
    return f"https://sermons.example.com/embed/{slug}"

def analyze_sermon_action(sermon_text: str, query: str, metadata: dict) -> dict:
    """
    Analyzes sermon text and returns a structured summary with metadata.
    Handles any arbitrary metadata fields.
    If the query requests a link (contains 'link'), includes an embed link.
    Args:
        sermon_text (str): The full sermon text.
        query (str): The user query.
        metadata (dict): Arbitrary metadata fields.
    Returns:
        dict: Structured summary with metadata and optional embed link.
    """
    # TODO: Implement actual sermon text analysis
    _ = sermon_text  # currently unused, placeholder for future implementation

    summary = "This sermon emphasizes the transformative power of forgiveness and redemption."
    themes = ["forgiveness", "redemption", "mercy"]
    emotional_tone = "inspiring"

    # Copy metadata to avoid mutating input
    meta_out = dict(metadata) if metadata else {}

    # Always ensure title is present for link generation
    title = meta_out.get("title", "sermon")
    # Add embed link if requested or not present
    include_link = "link" in query.lower()
    if include_link or not meta_out.get("reference_link"):
        meta_out["reference_link"] = generate_embed_link(title)

    # Always include embed_link if requested, otherwise only if present in metadata
    if include_link:
        meta_out["embed_link"] = meta_out["reference_link"]

    response = {
        "summary": summary,
        "themes": themes,
        "emotional_tone": emotional_tone,
        "metadata": meta_out
    }
    return response

# Example usage:
# sermon_text = "In this powerful sermon, we reflect on the transformative power of forgiveness and the beauty of redemption."
# query = "Please analyze this sermon and provide an embed link for the reference."
# metadata = {
#     "title": "Forgiveness and Redemption",
#     "speaker": "Pastor Mark",
#     "timestamp": "2023-02-10",
#     "custom_field": "Example value"
# }
# result = analyze_sermon_action(sermon_text, query, metadata)
# import json
# print(json.dumps(result, indent=2))
