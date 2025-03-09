import json
import re

def generate_embed_link(title: str) -> str:
    """
    Generate an embed link based on the sermon title.
    For example, "Forgiveness and Redemption" becomes:
    https://sermons.example.com/embed/forgiveness-and-redemption
    """
    # Create a slug by lowercasing and replacing non-alphanumeric characters with hyphens.
    slug = re.sub(r'\W+', '-', title.lower()).strip('-')
    return f"https://sermons.example.com/embed/{slug}"

def analyze_sermon_action(sermon_text: str, query: str, metadata: dict) -> dict:
    """
    Simulate a Custom GPT Action that analyzes sermon text using rich metadata and retrieval context.
    
    This action extracts a summary, themes, and an emotional tone from the sermon_text.
    It also integrates metadata such as title, speaker, and timestamp.
    
    If the reference (embed link) is not already present or if the user's query asks for a link,
    an embed link is generated and included in the final response.
    """
    # Placeholder analysis logic (simulate analysis)
    summary = "This sermon emphasizes the transformative power of forgiveness and redemption."
    themes = ["forgiveness", "redemption", "mercy"]
    emotional_tone = "inspiring"
    
    # Ensure metadata includes an embed link. If not provided, generate one.
    if not metadata.get("reference_link"):
        title = metadata.get("title", "sermon")
        metadata["reference_link"] = generate_embed_link(title)
    
    # Determine if the embed link should be included:
    # Include the embed link if the query mentions 'link' (case-insensitive)
    include_link = "link" in query.lower()
    
    # Build the final response with rich metadata
    response = {
        "summary": summary,
        "themes": themes,
        "emotional_tone": emotional_tone,
        "metadata": {
            "title": metadata.get("title", "Unknown Title"),
            "speaker": metadata.get("speaker", "Unknown Speaker"),
            "timestamp": metadata.get("timestamp", "Unknown Timestamp")
        }
    }
    
    if include_link:
        response["metadata"]["embed_link"] = metadata["reference_link"]
    
    return response

if __name__ == "__main__":
    # Example sermon text and metadata for testing the custom GPT action
    sermon_text = (
        "In this powerful sermon, we reflect on the transformative power of forgiveness and the beauty of redemption. "
        "We are reminded that every day offers a new chance to seek mercy and start anew."
    )
    query = "Please analyze this sermon and provide an embed link for the reference."
    metadata = {
        "title": "Forgiveness and Redemption",
        "speaker": "Pastor Mark",
        "timestamp": "2023-02-10",
        "reference_link": ""  # Empty indicates this is the first time a reference is made.
    }
    
    result = analyze_sermon_action(sermon_text, query, metadata)
    print("Custom GPT Action Result:")
    print(json.dumps(result, indent=2))
