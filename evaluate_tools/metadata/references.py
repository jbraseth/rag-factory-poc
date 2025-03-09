import spacy
from spacy.tokens import Span

# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

# ----------------------------
# Document-Level NER Extraction
# ----------------------------
text = "Apple is looking at buying U.K. startup for $1 billion."
doc = nlp(text)

print("Document-Level Entities:")
for ent in doc.ents:
    print(f"{ent.text} ({ent.start_char}, {ent.end_char}) - {ent.label_}")

# ----------------------------
# Token-Level Entity Information
# ----------------------------
print("\nToken-Level Entity Info:")
# For illustration, show info for the first two tokens
if len(doc) >= 2:
    print(f"Token: {doc[0].text}, IOB: {doc[0].ent_iob_}, Type: {doc[0].ent_type_}")
    print(f"Token: {doc[1].text}, IOB: {doc[1].ent_iob_}, Type: {doc[1].ent_type_}")

# ----------------------------
# Custom Entity Modification
# ----------------------------
# Example where the model misses "fb" as an organization
custom_text = "fb is hiring a new vice president of global policy."
doc_custom = nlp(custom_text)

print("\nBefore custom modification:", [(ent.text, ent.label_) for ent in doc_custom.ents])

# Find token "fb" and add it as an ORG entity
for token in doc_custom:
    if token.text.lower() == "fb":
        fb_ent = Span(doc_custom, token.i, token.i + 1, label="ORG")
        doc_custom.ents = list(doc_custom.ents) + [fb_ent]
        break

print("After custom modification:", [(ent.text, ent.label_) for ent in doc_custom.ents])
