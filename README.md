# ✨ RAG Factory POC — Second‑Brain Pipeline

A compact Retrieval‑Augmented Generation (RAG) stack that

* 🤝 **Learns with you** – Notebook LM & Readwise Reader
* 🗂️ **Stores documents, audio/video, and other media** – Whisper + Vectara keep page / timestamp metadata
* 💬 **Chats back inside Discord** – a small bot queries Vectara, calls an LLM and replies with inline citations

---

## 📚 Table of Contents

1. [Why this stack?](#why-this-stack)
2. [End‑to‑End Flow](#end-to-end-flow)
3. [Solution Architecture](#solution-architecture)
4. [Repository Layout](#repository-layout)
5. [Quick Start (example)](#quick-start-example)
6. [Roadmap](#roadmap)

---

## 🔎 Why this stack?

| Layer                          | Tool                                    | Role                                                                                                                                            |
| ------------------------------ | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Orientation / "Teach‑me first" | **Notebook LM**                         | One‑click Study Guide & Audio Overview for any PDF/Doc.                                                                                         |
| Deep reading & highlights      | **Readwise Reader**                     | Highlight, auto‑flashcards, nightly Markdown export.                                                                                            |
| Personal vault & linking       | **Obsidian**                            | Imported highlights live here; you write evergreen notes and connect them with `[[wikilinks]]`.                                                 |
| Audio → text                   | **Whisper CLI**                         | Transcribe audio/video → JSON with timestamps & optional speaker diarisation.                                                                   |
| Vector search & filters        | **Vectara**                             | Chunk & store text with metadata (`source_type`, `start_time`, `origin_page`, `speaker`).                                                       |
| Chat front‑end                 | **Discord Bot** (Python + `discord.py`) | User asks in a Discord channel; bot pulls passages from Vectara, calls OpenAI (or any LLM) and posts an answer with citations `(p …)` / `(t …)` |

---

## 🔄 End‑to‑End Flow

**Step 1 – Learn & Link**

1. Notebook LM generates a Study Guide ➜ saved in Obsidian.
2. Readwise Reader syncs your highlights ➜ Obsidian.
3. You enrich the vault with personal notes and `[[wikilinks]]`.

**Step 2 – Ingest**

1. Whisper transcribes new audio/video into JSON with timestamps.
2. A nightly script uploads both the Whisper output **and** any updated Markdown files from Obsidian to Vectara, attaching metadata (`origin_page`, `start_time`, `speaker`, …).

**Step 3 – Retrieve & Chat**

1. In Discord, you type `!ask <question>`.
2. The bot queries Vectara for the most relevant passages.
3. Passages are fed to an LLM (GPT‑4 o by default), which drafts an answer.
4. The bot posts the reply back to Discord with inline citations—e.g. `(p 142)` or `(t 00:10:30)`.

---

## 🛠 Solution Architecture

| Phase                         | Script / Tool                                               | Key output fields                                              |
| ----------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| 1 Transcription & Diarisation | `transcription/transcribe.py` (Whisper)  + `diarization.py` | `text`, `start_time`, `speaker`                                |
| 2 Metadata Enrichment         | `metadata/*.py`                                             | `topics`, `entities`, `sentiment`                              |
| 3 Upload to Vectara           | `vectara/upload.py`                                         | chunk text + metadata (`origin_page` or `start_time`)          |
| 4 Query Bridge & Bot          | `backend/query.py` + `bot/discord_bot.py`                   | 1) `/search` 2) build LLM prompt 3) post answer with citations |

### Metadata Cheat‑Sheet

* `source_type`: e.g. `book | highlight | transcript`
* `origin_page`: integer (for paginated docs)
* `start_time`: hh\:mm\:ss (for media)
* `speaker`, `topics[]`, `entities[]`, `sentiment`

---

## 📂 Repository Layout

```
.
├─ metadata/
│   ├─ references.py
│   ├─ topics.py
│   └─ sentiment.py
├─ transcription/
│   ├─ transcribe.py
│   ├─ diarization.py
│   └─ file_sharding.py
├─ vectara/
│   ├─ upload.py
│   └─ schema.json
├─ backend/
│   ├─ query.py            # Vectara ➜ LLM prompt builder
│   └─ config.example.env  # API keys & corpus IDs
├─ bot/
│   └─ discord_bot.py      # minimal discord.py client
└─ requirements.txt
```

---

## ⚡ Quick Start (example)

Below we ingest a **sermon audio file** and chat with it in Discord. Swap the file and prompts for any other material.

```bash
# 1 Configure API keys (Vectara, OpenAI, Discord Bot token)
cp backend/config.example.env .env && edit .env

# 2 Transcribe audio
python transcription/transcribe.py sermon.mp3

# 3 Optional: add metadata
python metadata/references.py data/sermon.json | \
python metadata/topics.py > data/sermon.enriched.json

# 4 Upload to Vectara
python vectara/upload.py data/sermon.enriched.json

# 5 Run the Discord bot (will join your server)
python bot/discord_bot.py
```

In Discord, type:

```
!ask Where does the speaker mention "trust"?
```

The bot responds with an answer and inline citations like `(t 00:10:30)` or `(p 142)`.

---

## 🗺️ Roadmap

* **β** – auto‑watch Obsidian folder; nightly Vectara upload.
* **1.0** – docker‑compose for Whisper + bot; slash‑command support.
* Future – domain‑specific enrichers, speaker clustering, sentiment dashboards.

---

### 🙌 Contributing

PRs welcome

MIT License   ·   © 2025 RAG Factory
