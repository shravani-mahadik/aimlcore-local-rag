
# AIMLCore Local Knowledge Assistant

A local Retrieval-Augmented Generation (RAG) based knowledge assistant that allows users to upload documents, index their content, search relevant information, and ask questions using a locally running Large Language Model.

The system uses **FastAPI**, **React + Vite**, **FAISS**, **embeddings**, and **Ollama with Llama 3.2:3b** to provide local document-based question answering.

---

## 🚀 Features

- 📄 Upload PDF documents
- 🔍 Extract text from PDF files
- ✂️ Split documents into smaller chunks
- 🧠 Generate vector embeddings
- 📦 Store embeddings using FAISS
- 🔎 Perform semantic similarity search
- 📚 Search across multiple indexed documents
- 💬 Ask questions using a RAG pipeline
- 🤖 Generate answers using local Ollama LLM
- 🔒 Keep the knowledge base and LLM processing local
- 📑 Display source documents and page numbers
- 🗑️ Delete uploaded documents and their indexes
- 📋 List uploaded documents
- 🌐 React-based web interface
- ⚡ FastAPI REST API

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │    Vite + Axios     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
       Document Upload                     User Question
              │                                 │
              ▼                                 ▼
       PDF Text Extraction              Query Embedding
              │                                 │
              ▼                                 ▼
           Chunking                     FAISS Retrieval
              │                                 │
              ▼                                 ▼
         Embeddings                    Relevant Chunks
              │                                 │
              ▼                                 ▼
         FAISS Index                    Grounded Prompt
                                                │
                                                ▼
                                      Ollama / Llama 3.2
                                                │
                                                ▼
                                         Final Answer
                                                │
                                                ▼
                                      Sources + Page Info
````

---

# 🛠️ Technologies Used

## Frontend

* React
* Vite
* JavaScript
* Axios
* Lucide React

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

## AI / Machine Learning

* Retrieval-Augmented Generation (RAG)
* Vector Embeddings
* FAISS
* Ollama
* Llama 3.2:3b

## Document Processing

* PDF text extraction
* Document chunking
* Metadata management

---

# 📁 Project Structure

```text
aimlcore-local-rag/
│
├── backend/
│   └── app/
│       ├── main.py
│       │
│       ├── api/
│       │   ├── chat.py
│       │   ├── search.py
│       │   └── documents.py
│       │
│       └── services/
│           ├── ingestion/
│           │   └── document_parser.py
│           │
│           ├── chunking/
│           │   └── chunker.py
│           │
│           ├── embeddings/
│           │   └── embedding_service.py
│           │
│           ├── retrieval/
│           │   ├── vector_store.py
│           │   └── multi_document_retriever.py
│           │
│           ├── indexing/
│           │   └── indexing_service.py
│           │
│           ├── rag/
│           │   └── rag_service.py
│           │
│           └── generation/
│               └── llm_service.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── uploads/
│   └── indexes/
│
├── tests/
│   ├── test_llm.py
│   ├── test_vector_persistence.py
│   └── test_indexing_service.py
│
├── venv/
│
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

## 1. Clone or open the project

Open PowerShell and navigate to the project directory:

```powershell
cd C:\Users\SAI\aimlcore-local-rag
```

---

## 2. Create virtual environment

If the virtual environment does not already exist:

```powershell
python -m venv venv
```

---

## 3. Activate virtual environment

For PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

You should see:

```text
(venv) PS C:\Users\SAI\aimlcore-local-rag>
```

---

## 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

Install Ollama and make sure it is running.

Check available models:

```powershell
ollama list
```

Pull the required model:

```powershell
ollama pull llama3.2:3b
```

Verify the model:

```powershell
ollama run llama3.2:3b
```

Test it:

```text
What is 2 + 2?
```

Expected:

```text
2 + 2 = 4.
```

Exit Ollama:

```text
/bye
```

---

# 🌐 Frontend Installation

Navigate to the frontend directory:

```powershell
cd C:\Users\SAI\aimlcore-local-rag\frontend
```

Install dependencies:

```powershell
npm install
```

The project uses:

```text
axios
lucide-react
```

If required:

```powershell
npm install axios lucide-react
```

---

# ▶️ Running the Project

The frontend and backend should be run in separate terminals.

---

## Terminal 1 — Backend

Open PowerShell:

```powershell
cd C:\Users\SAI\aimlcore-local-rag
```

Activate the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
uvicorn backend.app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — Frontend

Open another PowerShell window:

```powershell
cd C:\Users\SAI\aimlcore-local-rag\frontend
```

Start Vite:

```powershell
npm run dev
```

Frontend will normally run at:

```text
http://localhost:5173
```

Open this address in your browser.

---

# 📄 Document Upload Workflow

The document processing pipeline is:

```text
Upload PDF
     ↓
Save Document
     ↓
Generate SHA-256 Hash
     ↓
Generate Document ID
     ↓
Extract PDF Text
     ↓
Create Chunks
     ↓
Generate Embeddings
     ↓
Create FAISS Index
     ↓
Save Index + Metadata
```

Each indexed document is stored under:

```text
data/indexes/<document_id>/
```

The directory contains:

```text
index.faiss
metadata.json
```

---

# 🔎 Retrieval Workflow

When a user asks a question:

```text
User Question
      ↓
Query Embedding
      ↓
Search All FAISS Indexes
      ↓
Calculate Similarity
      ↓
Sort Results
      ↓
Select Top-K Results
```

The most relevant chunks are then passed to the RAG generation system.

---

# 💬 RAG Workflow

The complete RAG pipeline is:

```text
Question
   ↓
Multi-Document Retrieval
   ↓
Relevant Context
   ↓
Grounded Prompt
   ↓
Ollama Llama 3.2
   ↓
Answer
   ↓
Sources + Page Numbers
```

The LLM is instructed to answer using only the retrieved context.

If sufficient information is not available, the system is designed to respond:

```text
I could not find enough information in the uploaded knowledge base.
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /
```

Returns the API status.

---

## System Health

```http
GET /api/system/health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## Upload Document

```http
POST /api/documents/upload
```

Accepts document uploads.

Currently, PDF files are automatically indexed.

Supported upload extensions:

```text
.pdf
.docx
.txt
.md
.csv
```

---

## List Documents

```http
GET /api/documents
```

Returns the uploaded documents and their document IDs.

---

## Delete Document

```http
DELETE /api/documents/{document_id}
```

Deletes:

* Uploaded document
* FAISS index
* Associated metadata

---

## Semantic Search

```http
POST /api/search
```

Example request:

```json
{
  "question": "What position was I offered?",
  "top_k": 5
}
```

---

## RAG Chat

```http
POST /api/chat
```

Example request:

```json
{
  "question": "What position was I offered?",
  "top_k": 5
}
```

Example response:

```json
{
  "question": "What position was I offered?",
  "answer": "You were offered the position of AI/ML Engineer.",
  "sources": [
    {
      "chunk_id": "sample_document_001_chunk_0",
      "document_id": "sample_document_001",
      "page": 1,
      "similarity": 0.33
    }
  ],
  "source_count": 1
}
```

---

# 🧪 Testing

The project contains tests for important components.

## Test Ollama LLM

From the project root:

```powershell
python -m tests.test_llm
```

Expected result:

```text
===== OLLAMA LLM TEST =====

===== ANSWER =====
2 + 2 = 4

===== SUCCESS =====
```

---

## Test Vector Store Persistence

```powershell
python -m tests.test_vector_persistence
```

This verifies that the FAISS index and metadata can be saved and loaded successfully.

---

## Test Indexing Service

```powershell
python -m tests.test_indexing_service
```

This verifies the document indexing pipeline.

---

# 🖥️ User Interface

The React interface provides:

* Document upload
* Document list
* Delete document
* Chat interface
* AI responses
* Retrieved source information
* Page references
* Loading indicators
* Error handling

---

# 🔐 Local and Privacy-Focused Architecture

The project is designed around local processing.

The LLM runs through:

```text
Ollama
```

using:

```text
Llama 3.2:3b
```

The vector database is:

```text
FAISS
```

Therefore, the core document retrieval and LLM generation pipeline does not require sending document content to a hosted LLM API.

---

# 📊 Example

Suppose an uploaded document contains:

```text
We are delighted to offer you the position
of AI/ML Engineer at AIMLCore.
```

The user asks:

```text
What position was I offered?
```

The system:

```text
Question
   ↓
Embedding
   ↓
FAISS Search
   ↓
Relevant Document Chunk
   ↓
Grounded Prompt
   ↓
Llama 3.2
   ↓
AI/ML Engineer
```

The UI also displays the relevant source document and page.

---

# ⚠️ Current Limitations

* Automatic indexing is currently implemented for PDF documents.
* DOCX, TXT, MD and CSV upload support is present, but their indexing pipelines can be extended.
* FAISS indexes are stored locally.
* Ollama must be running locally for answer generation.
* The quality of answers depends on the quality of extracted text, embeddings, retrieval, and the selected LLM.

---

# 🔮 Future Enhancements

Possible future improvements include:

* DOCX indexing
* TXT indexing
* Markdown indexing
* CSV indexing
* Better document preview
* Streaming LLM responses
* Advanced metadata filtering
* Authentication and user accounts
* Conversation history
* Better citation formatting
* Hybrid keyword + semantic search
* Reranking retrieved chunks
* Docker deployment
* Cloud deployment
* Automated evaluation of RAG responses

---

# 👩‍💻 Project

**AIMLCore Local Knowledge Assistant**

### Main Technologies

```text
Python
FastAPI
React
Vite
FAISS
Embeddings
Ollama
Llama 3.2
RAG
Axios
```

---

# 📌 Conclusion

AIMLCore Local Knowledge Assistant demonstrates a complete local Retrieval-Augmented Generation pipeline.

It allows users to upload documents, convert their content into searchable vector representations, retrieve relevant information using FAISS, and generate grounded answers using a locally running Llama 3.2 model through Ollama.

The system combines document processing, semantic search, vector databases, LLM generation, and a modern web interface into a single local AI knowledge assistant.

```

Shravani Mahadik.