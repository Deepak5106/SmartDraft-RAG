# Smartdraft-RAG: 

A Retrieval-Augmented Generation (RAG) system designed to automate enterprise email workflows using structured corporate knowledge bases.

This project demonstrates how to build a semantic retrieval pipeline with intelligent context orchestration, enabling enterprise-grade AI-generated responses grounded in internal policy templates and operational documentation.

---

# 🚀 Key Features

## Dynamic Knowledge Ingestion Pipeline
- Automatically scans and parses localized `.txt` corporate knowledge files.
- Supports cold-start vector database reconstruction in cloud/container environments.
- Dynamically materializes embeddings from raw templates at runtime.

---

## Semantic Retrieval Optimization
- Uses vector embeddings via:
  - `sentence-transformers/all-MiniLM-L6-v2`
- Eliminates traditional keyword-search limitations by performing semantic similarity matching.
- Accurately maps ambiguous user scenarios to relevant compliance templates and enterprise policies.

---

## Contextual Prompt 
- Injects retrieved context directly into structured LLM instruction pipelines.
- Enforces:
  - corporate tone
  - formatting consistency
  - policy-safe response generation
  - controlled hallucination boundaries

---

## Persistent Resource Caching
- Uses Streamlit's:
  ```python
  @st.cache_resource
  ```
  for persistent in-memory caching.

Retains:
- vector database connections
- embedding model instances
- runtime resources
- cached LLM/runtime instances

Minimizes:
- repeated disk I/O
- embedding reload overhead
- cold query latency across concurrent sessions

---

# 🛠️ System Architecture

```
[User Scenario Input]
            │
            ▼
[HuggingFace Embeddings Engine]
            │
     (Vector Similarity Search)
            ▼
[Chroma Vector Database]
            │
   (Retrieves Top-K Contexts)
            ▼
[Hybrid Prompt Orchestration Layer]
            │
            ▼
[Groq Cloud LLM Engine]
            │
            ▼
[Generated Enterprise Email]
            │
            ▼
[Live Streamlit Frontend]
```

---

# 📋 Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestration Framework | LangChain |
| Community Integrations | LangChain-Community |
| Vector Store Adapter | LangChain-Chroma |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM Inference Engine | Llama 3.1 via Groq API |
| Deep Learning Runtime | Torch |
| Frontend UI | Streamlit |

---

# ⚙️ Installation & Setup

## Prerequisites
- Python 3.13(recommended)
- Valid Groq API Key 

## 1. Clone the Repository

```bash
git clone https://github.com/Deepak5106/SmartDraft-RAG.git
cd SmartDraft-RAG
```

## 2. Configure Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

## 3. Add Knowledge Base Files

Create a `data/` directory:

```bash
mkdir data
```

Place your raw enterprise templates and policy documents inside:

```
data/
├── compliance_policy.txt
└── enterprise_guidelines.txt
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Launch the Application

```bash
streamlit run step4_app.py
```

---

# 🔍 How the Pipeline Works

### Step 1 — Data Ingestion
The application scans all `.txt` files inside the `data/` directory.

### Step 2 — Embedding Generation
Each document is transformed into dense semantic vectors using:
- `all-MiniLM-L6-v2`

### Step 3 — Vector Storage
Generated embeddings are persisted inside:
- **ChromaDB** for low-latency semantic retrieval.

### Step 4 — User Query Processing
User scenarios are converted into embeddings and matched against stored enterprise templates using cosine similarity search.

### Step 5 — Context Injection
Top retrieved templates are dynamically injected into a structured orchestration prompt.

### Step 6 — LLM Generation
The contextualized prompt is sent to:
- **Llama 3.1 via Groq Cloud** to generate grounded enterprise email responses.

---

# 🔒 Security & Deployment Notes

## Data Isolation
Sensitive runtime artifacts are excluded using `.gitignore` policies:

```
.env
my_local_db/
data/
```

This prevents:
- API key exposure
- vector database leakage
- accidental credential commits

## Cloud Deployment Resilience
Includes fallback initialization routines that:
- detect missing vector databases
- automatically rebuild embeddings from raw templates
- materialize the semantic search space dynamically

This ensures smooth execution on:
- Streamlit Cloud
- containerized environments
- ephemeral compute instances

---

# 📈 Future Improvements
- Hybrid keyword + vector search for improved retrieval precision
- PDF/DOCX ingestion support for broader enterprise document compatibility
- Migration from monolithic Streamlit architecture to a decoupled frontend-backend system
- Dedicated REST API layer for scalable retrieval and generation workflows
- Webhook-based email ingestion pipeline for automatic real-time email fetching


---

# 🧠 Core Learning Concepts Demonstrated
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Embedding Pipelines
- Context Grounding
- LLM Hallucination Reduction
- Streamlit Resource Caching
- AI Workflow Engineering

---

# 👨‍💻 Author

Designed and developed by Deepak Maggo to demonstrate and utilize applications of Retrieval-Augmented Generation (RAG).