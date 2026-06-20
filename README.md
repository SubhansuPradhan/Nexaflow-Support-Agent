# 🚀 NexaFlow Persona-Adaptive Customer Support Agent

An intelligent AI-powered customer support system that detects customer personas, retrieves relevant knowledge using Retrieval-Augmented Generation (RAG), and generates persona-aware responses. Built entirely with local models using Ollama, ChromaDB, and Sentence Transformers, requiring no external API keys.

---

## 📌 Overview

NexaFlow Support Agent is a persona-adaptive customer support assistant designed for SaaS environments.

The system:

- Detects customer personas automatically
- Retrieves relevant documentation from a vector database
- Generates context-aware responses using RAG
- Adapts tone and communication style based on the user's persona
- Escalates unresolved or sensitive issues to human agents

Everything runs locally, ensuring privacy, low cost, and complete control over data.

---

## ✨ Features

### 🎭 Persona Detection

Automatically classifies users into:

- **Technical Expert**
- **Frustrated User**
- **Business Executive**

Each response is tailored to the detected persona.

### 📚 Retrieval-Augmented Generation (RAG)

- Semantic search using Sentence Transformers
- ChromaDB vector storage
- Top-k relevant document retrieval
- Grounded responses based on company documentation

### 🧠 Intelligent Response Generation

- Persona-specific prompts
- Context-aware answers
- Hallucination reduction through document grounding

### 🚨 Smart Escalation Engine

Escalates conversations when:

- No relevant documentation exists
- Confidence is low
- Legal or billing concerns are detected
- User frustration persists
- Sensitive topics arise

### 💬 Multi-Turn Conversations

- Session-based memory
- Context retention across interactions

### 📄 Human Handoff Summary

Generates structured JSON summaries including:

- Persona detected
- Issue description
- Retrieved documents
- Resolution attempts
- Escalation priority

---

## 🏗️ System Architecture

```text
User Query
    │
    ▼
┌─────────────────────┐
│ Persona Detector    │
│ (Ollama)            │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ RAG Retriever       │
│ (ChromaDB +         │
│ SentenceTransformers)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Response Generator  │
│ Persona-Aware LLM   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Escalation Engine   │
└────────┬────────────┘
         │
    ┌────┴─────┐
    │          │
 Normal    Escalated
 Reply      Handoff
```

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| LLM | Ollama (Llama 3.2) |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| PDF Generation | ReportLab |
| PDF Processing | PyPDF |
| CLI Output | Rich |
| Language | Python 3.10+ |

---

## 🔍 Persona Detection

The system uses an Ollama-powered classifier that returns:

```json
{
  "persona": "TECHNICAL_EXPERT",
  "confidence": 0.92,
  "reasoning": "User references APIs and technical errors."
}
```

### Supported Personas

| Persona | Characteristics |
|----------|----------------|
| Technical Expert | Technical terminology, APIs, debugging |
| Frustrated User | Emotional language, repeated issues |
| Business Executive | Business impact, timelines, outcomes |

### Fallback Classification

If JSON output fails, a keyword-based classifier ensures uninterrupted operation.

---

## 📚 RAG Pipeline

### Chunking Strategy

- Paragraph-based chunking
- Chunk Size: **500 characters**
- Overlap: **60 characters**

### Embedding Model

```text
all-MiniLM-L6-v2
```

Benefits:

- Lightweight (~80MB)
- Fast inference
- Strong semantic retrieval performance

### Vector Database

**ChromaDB**

Configuration:

```text
Distance Metric: Cosine Similarity
Persistence: Local Disk
Storage: ./chroma_db
```

### Retrieval Flow

1. User query embedding
2. Similarity search
3. Top-4 chunk retrieval
4. Context injection into LLM prompt
5. Persona-aware response generation

---

## 🚨 Escalation Logic

| Signal | Priority |
|----------|----------|
| No Relevant Documents | Low |
| Low Confidence Retrieval | Low |
| Billing/Legal Keywords | High |
| Turn Limit Reached | Medium |
| Repeated Frustration | Medium |
| Sensitive Topics | High |

Escalation priority is determined by the highest triggered signal.

---

## 📂 Knowledge Base

The system ships with **16 support documents** covering:

- Account Management
- Authentication
- API Documentation
- Billing & Payments
- Rate Limits
- Webhooks
- Security & Privacy
- Team Management
- Integrations
- Data Export
- FAQs
- Refund Policies

Supported formats:

- Markdown (.md)
- PDF (.pdf)

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Ollama installed
- 8GB+ RAM recommended

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/nexaflow-support-agent.git
cd nexaflow-support-agent
```

---

### 2️⃣ Install Ollama

Download:

https://ollama.com/download

Pull the model:

```bash
ollama pull llama3.2
```

Verify installation:

```bash
ollama run llama3.2 "hello"
```

---

### 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Build Vector Database

```bash
python scripts/ingest_documents.py
```

This process:

- Loads all support documents
- Creates semantic chunks
- Generates embeddings
- Stores vectors in ChromaDB

---

### 6️⃣ Run Application

#### Streamlit UI

```bash
streamlit run src/ui/streamlit_app.py
```

Application:

```text
http://localhost:8501
```

#### CLI Mode

```bash
python main.py
```

---

## 📸 Example Queries

### Technical Expert

```text
I'm receiving NF-1004 during token refresh.
OAuth succeeds initially but fails after one hour.
```

### Frustrated User

```text
I've been trying to log in for three days.
Nothing works and I've tried everything.
```

### Business Executive

```text
Our dashboard has been unavailable since this morning.
What is the expected resolution timeline?
```

### Escalation Example

```text
I want a refund immediately or I'll contact my lawyer.
```

---

## 📊 Future Improvements

- Multi-language support
- Hybrid search (BM25 + Vector Search)
- LangGraph multi-agent workflows
- Redis-based persistent memory
- Fine-tuned persona classifier
- Real-time document reindexing
- Advanced analytics dashboard

---

## ⚠️ Current Limitations

- English-only support
- Session-based memory only
- Manual document re-ingestion
- Single-agent architecture
- Local LLM quality depends on hardware

---

## 🎯 Key Learnings

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Local LLM Deployment
- Persona-Based Prompt Engineering
- Intelligent Escalation Workflows
- Streamlit Application Development

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

## 👨‍💻 Author

**Subhansu Pradhan**

Data Science & AI Engineering Enthusiast

If you found this project useful, consider giving it a ⭐ on GitHub.
