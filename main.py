"""
Main entry point for the RAG Pipeline POC.
Processes sermon audio, extracts metadata, stores in vector DB, and retrieves context.
"""

from evaluate_tools.transcription.file_sharding import split_audio
from evaluate_tools.transcription.transcribe import transcribe_audio
from evaluate_tools.transcription.diarization import diarize_speakers
from evaluate_tools.metadata.references import nlp as spacy_nlp
from evaluate_tools.metadata.sentiment import analyze_sentiment
from evaluate_tools.metadata.topics import extract_topics
from evaluate_tools.vector_database import db_client
from evaluate_tools.rag.retrieval import SermonVectorDB
from evaluate_tools.rag.custom_gpt_actions import analyze_sermon_action


def main(audio_path, user_query):
    """
    Runs the full RAG pipeline: splits audio, transcribes, diarizes, extracts metadata,
    stores in Weaviate, retrieves relevant segments, and generates a GPT-enhanced response.
    """
    chunk_files = split_audio(audio_path, chunk_length_minutes=10)

    transcripts = []
    diarizations = []
    metadatas = []

    # First, collect all transcripts and diarizations
    for idx, chunk_file in enumerate(chunk_files):
        transcript_text, _ = transcribe_audio(chunk_file)
        transcripts.append(transcript_text)
        diarization_result = diarize_speakers(chunk_file, transcript=transcript_text)
        diarizations.append(diarization_result)

    # Now, run BERTopic on all chunk transcripts together (if more than 1 chunk)
    if len(transcripts) > 1:
        topic_infos = extract_topics(transcripts, n_topics=3)
    else:
        topic_infos = [["Not enough data for topic modeling"] for _ in transcripts]

    # Now, process each chunk for metadata and DB storage
    for idx, transcript_text in enumerate(transcripts):
        doc = spacy_nlp(transcript_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        topic_info = topic_infos[idx]
        sentiment = analyze_sentiment(transcript_text)

        metadata = {
            "entities": entities,
            "topics": topic_info,
            "sentiment": sentiment
        }
        metadatas.append(metadata)

        sermon_object = {
            "title": f"Sermon Chunk {idx}",
            "content": transcript_text
        }
        db_client.client.data_object.create(sermon_object, "Sermon")  # pylint: disable=no-member

    # Use SermonVectorDB for retrieval (loads from pipeline data)
    vector_db = SermonVectorDB()
    results = vector_db.search_sermons(user_query)

    # Use the top result for GPT action, if available
    if results and "text" in results[0]:
        selected_text = results[0]["text"]
        selected_metadata = results[0].get("metadata", {})
    else:
        selected_text = ""
        selected_metadata = {}

    # Merge with fallback metadata
    metadata = {
        "title": selected_metadata.get("title", "Sermon"),
        "speaker": selected_metadata.get("speaker", "Unknown"),
        "timestamp": selected_metadata.get("timestamp", "Unknown"),
        "reference_link": selected_metadata.get("reference_link", ""),
    }
    final_response = analyze_sermon_action(selected_text, user_query, metadata)
    print("Final RAG Pipeline Response:")
    print(final_response)

if __name__ == "__main__":
    # Example usage
    main("data/sermons/2025_5_11_Podcast.mp3", "What does the sermon say about peace?")
