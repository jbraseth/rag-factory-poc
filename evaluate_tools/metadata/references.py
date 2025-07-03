"""
Extracts scripture/book references from a sermon transcript using spaCy NER and regex backup.
"""

import re
import spacy


# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

# List of common Bible books for regex matching
BIBLE_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

# Regex pattern for scripture references (e.g., John 3:16, 1 Corinthians 13:4-7)
BOOKS_PATTERN = "|".join([re.escape(book) for book in BIBLE_BOOKS])
SCRIPTURE_REGEX = re.compile(
    rf"\b({BOOKS_PATTERN})\s+\d{{1,3}}(?::\d{{1,3}}(?:-\d{{1,3}})?(?:,\s*\d{{1,3}}(?::\d{{1,3}})?)*)?\b",
    re.IGNORECASE
)

def extract_scripture_references(transcript):
    """
    Takes a sermon transcript as input and returns a list of detected scripture or book references
    using spaCy NER and regex as backup.
    Args:
        transcript (str): The sermon transcript text.
    Returns:
        List[str]: List of detected scripture or book references.
    """
    doc = nlp(transcript)
    references = set()

    # 1. Use spaCy NER to find book names (ORG, WORK_OF_ART, etc.)
    for ent in doc.ents:
        if ent.label_ in {"WORK_OF_ART", "ORG", "PERSON"}:
            for book in BIBLE_BOOKS:
                if ent.text.lower().startswith(book.lower()):
                    match = SCRIPTURE_REGEX.search(transcript, ent.start_char)
                    if match:
                        references.add(match.group(0))
                    else:
                        references.add(book)
                    break

    # 2. Use regex as backup for missed references
    for match in SCRIPTURE_REGEX.finditer(transcript):
        references.add(match.group(0))

    return sorted(references)

# Example usage:
# transcript = "Today we read from John 3:16 and 1 Corinthians 13:4-7. The book of Genesis is also referenced."
# print(extract_scripture_references(transcript))
