# **RAG Pipeline POC – Design & Architecture**

This project is the **first phase of a proof-of-concept (POC) for a Retrieval-Augmented Generation (RAG) pipeline** focused on processing sermon data. The goal is to build an **intelligent, metadata-aware retrieval system** that enhances sermon searchability and contextual analysis.  

This phase primarily defines the **architecture and components** rather than providing a fully integrated system. Future iterations will refine retrieval accuracy, improve scalability, and enhance domain-specific AI interactions.

---

## **📌 Table of Contents**
- [Project Overview](#project-overview)
- [Solution Architecture](#solution-architecture)
- [File Mapping](#file-mapping)
- [Future Directions](#future-directions)

---

## **🚀 Project Overview**
This POC outlines an **end-to-end AI-driven sermon retrieval pipeline** with the following core objectives:

✅ **Transcribe & Identify Speakers** → Convert sermon audio to text and label speakers.  
✅ **Extract Metadata** → Identify entities, topics, and sentiment from transcripts.  
✅ **Index & Store Sermon Data** → Use a **vector database** (Weaviate) for **semantic search** and metadata filtering.  
✅ **Retrieve Contextual Insights** → Employ **LlamaIndex** to fetch relevant sermon segments based on user queries.  
✅ **Enhance Responses** → Integrate **Custom GPT Actions** to dynamically generate embed links, timestamps, and speaker attributions.  

This design ensures **retrieved sermon excerpts are rich with context**, improving accuracy in AI-generated responses.

---

## **🛠 Solution Architecture**
This modular solution integrates multiple AI components, each handling a **distinct phase** of the processing pipeline.

### **1️⃣ Transcription & Speaker Identification**
- **Tools Used:** OpenAI Whisper, SpeechBrain
- **Purpose:** Converts sermon **audio into text** and **labels speakers**.
- **Example Output:**  
   ```json
   {
       "text": "Faith is trusting in what you cannot see.",
       "speaker": "John Mark Comer",
       "timestamp": "00:10:30"
   }
   ```

### **2️⃣ Metadata Extraction & Enrichment**
- **Tools Used:** spaCy (NER), BERTopic (topics), Hugging Face (sentiment)
- **Purpose:** Identifies **key entities, topics, sentiment, and scripture references** from sermon transcripts.
- **Example Metadata Fields:**  
   ```json
   {
       "topics": ["Faith", "Courage"],
       "bible_references": ["Matthew 14:27"],
       "sentiment": "Encouraging"
   }
   ```

### **3️⃣ Vector Storage & Retrieval**
- **Tools Used:** Weaviate, LlamaIndex
- **Purpose:** Stores **sermon embeddings** and **metadata** for **fast, contextual retrieval**.
- **Retrieval Example:**  
   ```json
   {
       "query": "What does John Mark Comer say about faith?",
       "retrieved_segments": [
           {
               "text": "Faith is trusting in what you cannot see.",
               "timestamp": "00:10:30",
               "bible_references": ["Matthew 14:27"]
           }
       ]
   }
   ```

### **4️⃣ Contextual Response Generation**
- **Tools Used:** OpenAI’s Custom GPT Actions
- **Purpose:** Enhances **retrieved sermon excerpts** with structured metadata before passing them to the language model.
- **Example Enhancement:**  
   ```text
   "John Mark Comer (Bridgetown Church) spoke on 'Faith' at timestamp 10:30. [Watch the full sermon here](SERMON_LINK)"
   ```

---

## **📂 File Mapping**
This section details where each component resides in the project structure.

### **🔹 Metadata Processing**
| File | Description |
|------|-------------|
| [`metadata/references.py`](evaluate_tools/metadata/references.py) | Named Entity Recognition (NER) for identifying books, people, locations. |
| [`metadata/sentiment.py`](evaluate_tools/metadata/sentiment.py) | Sentiment analysis to classify emotional tone. |
| [`metadata/topics.py`](evaluate_tools/metadata/topics.py) | Topic modeling with BERTopic to classify sermon themes. |

### **🔹 RAG Pipeline & Retrieval**
| File | Description |
|------|-------------|
| [`rag/custom_gpt_actions.json`](evaluate_tools/rag/custom_gpt_actions.json) | Schema for Custom GPT actions to enhance retrieval responses. |
| [`rag/custom_gpt_actions.py`](evaluate_tools/rag/custom_gpt_actions.py) | Implements Custom GPT actions for metadata integration. |
| [`rag/retrieval.py`](evaluate_tools/rag/retrieval.py) | LlamaIndex-based retrieval POC for fetching relevant sermon segments. |

### **🔹 Transcription & Speaker Diarization**
| File | Description |
|------|-------------|
| [`transcription/transcribe.py`](evaluate_tools/transcription/transcribe.py) | Converts sermon audio to text using OpenAI Whisper. |
| [`transcription/diarization.py`](evaluate_tools/transcription/diarization.py) | Identifies and labels speakers using SpeechBrain. |
| [`transcription/file_sharding.py`](evaluate_tools/transcription/file_sharding.py) | Splits long audio files into smaller chunks for processing. |

### **🔹 Vector Database & Semantic Search**
| File | Description |
|------|-------------|
| [`vector_database/db_client.py`](evaluate_tools/vector_database/db_client.py) | Connects to Weaviate for vector search and metadata storage. |
| [`vector_database/SETUP_DB.MD`](evaluate_tools/vector_database/SETUP_DB.MD) | Step-by-step guide for setting up Weaviate with Docker Compose. |
| [`vector_database/setup_db.sh`](evaluate_tools/vector_database/setup_db.sh) | Bash script to automate Weaviate setup locally. |

### **🔹 Dependencies**
| File | Description |
|------|-------------|
| [`requirements.txt`](evaluate_tools/requirements.txt) | Lists all necessary Python packages for this project. |

---

## **🚀 Future Directions**
The **next steps** for this project focus on **expanding retrieval accuracy** and **integrating all components into a unified pipeline.**

### **📌 Immediate Priorities**
✅ **Connect & test the end-to-end pipeline** → Ensure **retrieved sermon excerpts align with user queries**.  
✅ **Refine metadata extraction** → Improve **scripture detection & topic modeling accuracy**.  
✅ **Optimize retrieval efficiency** → Fine-tune **query filtering & chunking strategies**.  

### **📌 Long-Term Goals**
🔹 **Scale storage to support thousands of sermons.**  
🔹 **Enhance retrieval precision with metadata-aware ranking.**  
🔹 **Deploy as an API for broader accessibility.**  
🔹 **Integrate with a front-end UI for user-friendly sermon search.**  

---

## **💡 Final Thoughts**
This **RAG POC** sets the foundation for **intelligent, context-driven sermon retrieval** by combining **AI transcription, metadata extraction, vector search, and LlamaIndex-powered retrieval.**  

By refining this framework, we can **build a scalable, AI-enhanced knowledge base for sermon analysis.** 🔥  

---

### **🛠 Want to Contribute?**
Feel free to submit **feature suggestions, code optimizations, or bug fixes** to improve retrieval accuracy & metadata processing. 🚀  

Would you like me to draft a **step-by-step installation guide** to accompany this? Let me know! 🎯
