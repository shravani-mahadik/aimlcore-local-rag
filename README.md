# 🤖 AIMLCore Local RAG – Knowledge Assistant

AIMLCore Local RAG is a **local Retrieval-Augmented Generation (RAG) knowledge assistant** that allows users to upload documents and ask questions about their content.

The system extracts text from documents, divides the content into chunks, generates vector embeddings, stores them using **FAISS**, retrieves the most relevant information, and generates grounded answers using a **local Ollama LLM**.

---

## 🚀 Features

- 📄 Upload PDF, DOCX, TXT, Markdown and CSV documents
- 🔍 Semantic search using vector embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- 📚 Multi-document knowledge retrieval
- ⚡ FAISS vector database for fast similarity search
- 🤖 Local LLM using Ollama
- 🔐 Local document processing
- 📌 Source and page information in answers
- 🗑️ Delete uploaded documents
- 🌐 FastAPI backend
- 💻 React + Vite frontend
- 🧪 Automated tests
- 📊 Evaluation support

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    │ Ask Question / Upload│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ React Frontend       │
                    │ Vite + JavaScript     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ FastAPI Backend      │
                    │ REST API             │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ Document        │        │ Question         │
        │ Indexing        │        │ Processing       │
        └────────┬────────┘        └────────┬─────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ Text Extraction │        │ Query Embedding  │
        └────────┬────────┘        └────────┬─────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ Text Chunking   │        │ FAISS Retrieval  │
        └────────┬────────┘        └────────┬─────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ Embeddings      │        │ Relevant Chunks  │
        └────────┬────────┘        └────────┬─────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌──────────────────┐
        │ FAISS Index     │───────▶│ Grounded Prompt  │
        └─────────────────┘        └────────┬─────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │ Ollama LLM       │
                                  │ llama3.2:3b      │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │ Answer + Sources │
                                  └──────────────────┘
````

---

## 🔄 RAG Workflow

The application follows this pipeline:

```text
Document Upload
      ↓
Document Validation
      ↓
PDF Text Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Index
      ↓
Document Storage
      ↓
User Question
      ↓
Query Embedding
      ↓
Search Across Documents
      ↓
Top-K Relevant Chunks
      ↓
Grounded Prompt
      ↓
Ollama LLM
      ↓
Answer + Sources
```

---

## 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* FAISS
* Sentence Embeddings
* PyPDF
* Requests

### Frontend

* React
* Vite
* JavaScript
* CSS

### AI / ML

* Retrieval-Augmented Generation (RAG)
* Vector Embeddings
* FAISS Similarity Search
* Ollama
* Llama 3.2 3B

### Testing

* Pytest

---

## 📁 Project Structure

```text
aimlcore-local-rag/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── chat.py
│       │   ├── search.py
│       │   └── documents.py
│       │
│       ├── services/
│       │   ├── chunking/
│       │   ├── embeddings/
│       │   ├── generation/
│       │   ├── indexing/
│       │   ├── ingestion/
│       │   ├── rag/
│       │   └── retrieval/
│       │
│       └── main.py
│
├── data/
│   ├── uploads/
│   └── indexes/
│
├── evaluation/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/aimlcore-local-rag.git
```

Move into the project directory:

```bash
cd aimlcore-local-rag
```

---

## 2. Create Python Virtual Environment

```bash
python -m venv venv
```

### Windows PowerShell

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install and Run Ollama

The project uses **Ollama** to run the local LLM.

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

Start Ollama:

```bash
ollama serve
```

The application expects Ollama to be available at:

```text
http://localhost:11434
```

---

# ▶️ Running the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

The FastAPI server will normally be available at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

# ▶️ Running the Frontend

Open another terminal.

Move to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 📄 Document Upload

Users can upload supported documents through the web interface.

Supported formats:

```text
PDF
DOCX
TXT
MD
CSV
```

For PDF files, the indexing pipeline performs:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
FAISS Index
```

The generated index is stored locally.

---

# 💬 Asking Questions

After uploading and indexing documents, users can ask questions such as:

```text
What position was I offered?
```

```text
What is the start date?
```

```text
What is the work arrangement?
```

The system searches across the indexed documents and returns an answer based on the retrieved context.

---

# 🔎 Multi-Document Retrieval

The project supports searching across multiple indexed documents.

The retrieval process:

```text
User Question
      ↓
Query Embedding
      ↓
Search Every Document Index
      ↓
Collect Results
      ↓
Sort by Similarity
      ↓
Global Top-K Results
```

This allows the assistant to use information from multiple uploaded documents.

---

# 🧠 Grounded Generation

The LLM is instructed to answer using only the retrieved document context.

The system follows these principles:

* Do not invent facts
* Do not use outside knowledge
* Use the provided document context
* Provide source information
* Include page information when available
* Clearly explain conflicting sources
* State when sufficient information cannot be found

This helps reduce unsupported answers.

---

# 📚 Sources

The assistant displays retrieved source information including:

```text
Document ID
Page
Chunk ID
Similarity Score
Content
```

Example:

```text
Source: doc_1df29822e1a9
Page: 1
Similarity: 0.296
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /
```

Returns the application status.

---

## System Health

```http
GET /api/system/health
```

Checks whether the backend is running.

---

## Upload Document

```http
POST /api/documents/upload
```

Uploads and indexes a supported document.

---

## List Documents

```http
GET /api/documents
```

Returns uploaded documents.

---

## Delete Document

```http
DELETE /api/documents/{document_id}
```

Deletes the uploaded document and its associated FAISS index.

---

## Search

```http
POST /api/search
```

Performs semantic search over the knowledge base.

Example request:

```json
{
    "question": "What position was I offered?",
    "top_k": 5
}
```

---

## Chat

```http
POST /api/chat
```

Runs the complete RAG pipeline and generates an answer.

Example request:

```json
{
    "question": "What position was I offered?",
    "top_k": 5
}
```

---

# 🧪 Running Tests

Run the test suite using:

```bash
pytest
```

The tests cover components such as:

* Document parsing
* Text chunking
* Embeddings
* Indexing
* Retrieval
* RAG pipeline
* Ollama integration

---

# 🔐 Privacy

A major goal of this project is local document processing.

Documents are processed locally and the LLM is accessed through a local Ollama instance.

No external cloud LLM API is required for the generation component.

---

# 📌 Important Notes

The `.gitignore` file excludes local/generated resources such as:

```text
venv/
indexes/
data/uploads/
data/indexes/
node_modules/
.env
```

These files should not be committed to GitHub.

After cloning the repository, create the required local environment and indexes again.

---

# 🚀 Future Improvements

Possible future enhancements include:

* Support for DOCX, TXT, Markdown and CSV indexing
* Improved document metadata management
* Streaming LLM responses
* Conversation history
* Better source citation UI
* Advanced filtering by document
* Reranking retrieved chunks
* Authentication
* Docker deployment
* Cloud deployment
* Improved evaluation metrics
* Better error handling and logging

---

# 👩‍💻 Author

**Shravani Mahadik**

Computer Engineering
AI/ML Enthusiast | Python Developer | Machine Learning

---

# ⭐ Project

**AIMLCore Local RAG – Knowledge Assistant**

A local AI-powered knowledge assistant built using:

```text
Python
FastAPI
React
FAISS
Embeddings
Ollama
Llama 3.2
RAG
```

If you find this project useful, consider giving the repository a ⭐ on GitHub.

````
