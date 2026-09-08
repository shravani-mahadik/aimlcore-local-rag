import { useEffect, useState } from "react";
import axios from "axios";
import {
  Send,
  Upload,
  FileText,
  Bot,
  User,
  Plus,
  Trash2,
  LoaderCircle,
} from "lucide-react";

import "./App.css";


const API_URL = "http://127.0.0.1:8000";


function App() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [file, setFile] = useState(null);

  const [documents, setDocuments] = useState([]);

  const [uploading, setUploading] = useState(false);

  const [uploadMessage, setUploadMessage] = useState("");

  const [uploadError, setUploadError] = useState("");


  // =========================================
  // LOAD DOCUMENTS
  // =========================================

  const loadDocuments = async () => {

    try {

      const response = await axios.get(
        `${API_URL}/api/documents`
      );

      setDocuments(
        response.data.documents || []
      );

    } catch (error) {

      console.error(
        "Could not load documents:",
        error
      );

    }
  };


  // =========================================
  // LOAD DOCUMENTS WHEN APP STARTS
  // =========================================

  useEffect(() => {

    loadDocuments();

  }, []);


  // =========================================
  // ASK QUESTION
  // =========================================

  const askQuestion = async () => {

    if (!question.trim() || loading) {
      return;
    }

    const userQuestion = question.trim();

    setQuestion("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setLoading(true);

    try {

      const response = await axios.post(
        `${API_URL}/api/chat`,
        {
          question: userQuestion,
          top_k: 5,
        }
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: response.data.answer,
          sources: response.data.sources || [],
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I could not connect to the knowledge assistant. Make sure the FastAPI server is running.",
          sources: [],
        },
      ]);

    } finally {

      setLoading(false);

    }
  };


  // =========================================
  // ENTER KEY
  // =========================================

  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();

    }
  };


  // =========================================
  // NEW CHAT
  // =========================================

  const newChat = () => {

    setMessages([]);

    setQuestion("");

  };


  // =========================================
  // UPLOAD DOCUMENT
  // =========================================

  const handleFileChange = async (event) => {

    const selectedFile =
      event.target.files?.[0];

    if (!selectedFile) {
      return;
    }


    setFile(selectedFile);

    setUploadMessage("");

    setUploadError("");

    setUploading(true);


    try {

      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );


      const response = await axios.post(
        `${API_URL}/api/documents/upload`,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );


      const result = response.data;


      if (result.status === "indexed") {

        setUploadMessage(
          `${selectedFile.name} uploaded and indexed successfully.`
        );

      } else if (
        result.status === "duplicate"
      ) {

        setUploadMessage(
          `${selectedFile.name} already exists.`
        );

      } else if (
        result.indexing_status === "failed"
      ) {

        setUploadError(
          `Upload succeeded, but indexing failed: ${
            result.error || "Unknown error"
          }`
        );

      } else {

        setUploadMessage(
          `${selectedFile.name} uploaded successfully.`
        );

      }


      // Refresh document list

      await loadDocuments();


    } catch (error) {

      console.error(
        "Upload error:",
        error
      );


      let errorMessage =
        "Could not upload the document.";


      if (
        error.response?.data?.detail
      ) {

        errorMessage =
          error.response.data.detail;

      }


      setUploadError(
        errorMessage
      );

    } finally {

      setUploading(false);

    }
  };


  // =========================================
  // DELETE DOCUMENT
  // =========================================

  const deleteDocument = async (
    documentId
  ) => {

    try {

      await axios.delete(
        `${API_URL}/api/documents/${documentId}`
      );

      await loadDocuments();

    } catch (error) {

      console.error(
        "Delete error:",
        error
      );

    }
  };


  return (
    <div className="app">


      {/* ======================================
          SIDEBAR
      ======================================= */}

      <aside className="sidebar">


        {/* BRAND */}

        <div className="brand">

          <div className="brand-icon">

            <Bot size={22} />

          </div>

          <div>

            <h2>AIMLCore</h2>

            <span>
              Local Knowledge
            </span>

          </div>

        </div>


        {/* NEW CHAT */}

        <button
          className="new-chat"
          onClick={newChat}
        >

          <Plus size={18} />

          New Chat

        </button>


        {/* DOCUMENTS */}

        <div className="sidebar-section">

          <div className="section-title">

            <span>
              DOCUMENTS
            </span>

          </div>


          {documents.length === 0 ? (

            <div className="document-empty">

              No documents uploaded

            </div>

          ) : (

            documents.map(
  (document, index) => (
    <div
      className="document-item"
      key={document.document_id || index}
    >
      <FileText size={18} />

      <div className="document-info">
        <span
          title={document.filename}
        >
          {document.filename}
        </span>

        <small>
          Indexed document
        </small>
      </div>

      <button
        className="delete-button"
        onClick={() => {
          const confirmed = window.confirm(
            `Delete "${document.filename}"?`
          );

          if (confirmed) {
            deleteDocument(
              document.document_id
            );
          }
        }}
        title="Delete document"
        aria-label={`Delete ${document.filename}`}
      >
        <Trash2 size={17} />
      </button>
    </div>
  )
)
          )}

        </div>


        {/* UPLOAD */}

        <label
          className={`upload-button ${
            uploading
              ? "uploading"
              : ""
          }`}
        >

          {uploading ? (

            <LoaderCircle
              size={18}
              className="spin"
            />

          ) : (

            <Upload size={18} />

          )}


          <span>

            {uploading
              ? "Indexing..."
              : "Upload Document"}

          </span>


          <input
            type="file"
            accept=".pdf,.txt,.docx,.md,.csv"
            onChange={
              handleFileChange
            }
            disabled={uploading}
            hidden
          />

        </label>


        {/* SELECTED FILE */}

        {file && (

          <div className="selected-file">

            <FileText size={16} />

            <span>
              {file.name}
            </span>

          </div>

        )}


        {/* SUCCESS MESSAGE */}

        {uploadMessage && (

          <div className="upload-success">

            ✓ {uploadMessage}

          </div>

        )}


        {/* ERROR MESSAGE */}

        {uploadError && (

          <div className="upload-error">

            ✕ {uploadError}

          </div>

        )}


        {/* FOOTER */}

        <div className="sidebar-footer">

          <span>
            Local RAG System
          </span>

          <span>
            v1.0
          </span>

        </div>

      </aside>


      {/* ======================================
          MAIN
      ======================================= */}

      <main className="main">


        {/* TOPBAR */}

        <header className="topbar">

          <div>

            <h1>
              Knowledge Assistant
            </h1>

            <p>
              Ask questions about your documents
            </p>

          </div>


          <div className="status">

            <span className="status-dot"></span>

            Local AI Online

          </div>

        </header>


        {/* ====================================
            CHAT AREA
        ===================================== */}

        <section className="chat-area">


          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-icon">

                <Bot size={32} />

              </div>


              <h2>
                How can I help you?
              </h2>


              <p>
                Ask a question about your
                uploaded documents.
              </p>


              <div className="suggestions">


                <button
                  onClick={() =>
                    setQuestion(
                      "What position was I offered?"
                    )
                  }
                >

                  What position was I offered?

                </button>


                <button
                  onClick={() =>
                    setQuestion(
                      "What is the start date?"
                    )
                  }
                >

                  What is the start date?

                </button>


                <button
                  onClick={() =>
                    setQuestion(
                      "What is the work arrangement?"
                    )
                  }
                >

                  What is the work arrangement?

                </button>


              </div>

            </div>

          ) : (


            <div className="messages">


              {messages.map(
                (message, index) => (

                  <div
                    className={`message ${
                      message.role
                    }`}
                    key={index}
                  >


                    <div className="avatar">

                      {message.role ===
                      "user" ? (

                        <User size={18} />

                      ) : (

                        <Bot size={18} />

                      )}

                    </div>


                    <div className="message-content">


                      <div className="message-label">

                        {message.role ===
                        "user"
                          ? "You"
                          : "AIMLCore Assistant"}

                      </div>


                      <div className="message-text">

                        {message.content}

                      </div>


                      {message.sources?.length >
                        0 && (

                        <div className="sources">


                          <div className="sources-title">

                            <FileText
                              size={15}
                            />

                            Sources

                          </div>


                          {message.sources.map(
                            (
                              source,
                              sourceIndex
                            ) => (

                              <div
                                className="source-card"
                                key={
                                  sourceIndex
                                }
                              >

                                <div>

                                  <strong>
                                    {
                                      source.document_id
                                    }
                                  </strong>

                                  <span>
                                    Page{" "}
                                    {
                                      source.page
                                    }
                                  </span>

                                </div>


                                <span className="source-page">
                                  Page {source.page}
                                </span>
                                  

                              </div>

                            )
                          )}

                        </div>

                      )}

                    </div>

                  </div>

                )
              )}


              {loading && (

                <div className="message assistant">


                  <div className="avatar">

                    <Bot size={18} />

                  </div>


                  <div className="message-content">


                    <div className="message-label">

                      AIMLCore Assistant

                    </div>


                    <div className="loading">

                      <LoaderCircle
                        size={18}
                        className="spin"
                      />

                      Thinking...

                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>


        {/* ====================================
            INPUT
        ===================================== */}

        <div className="input-wrapper">


          <div className="input-box">


            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(
                  event.target.value
                )
              }
              onKeyDown={
                handleKeyDown
              }
              placeholder="Ask something about your documents..."
              rows={1}
            />


            <button
              className="send-button"
              onClick={askQuestion}
              disabled={
                !question.trim() ||
                loading
              }
            >

              {loading ? (

                <LoaderCircle
                  size={20}
                  className="spin"
                />

              ) : (

                <Send size={20} />

              )}

            </button>

          </div>


          <p className="input-hint">

            Answers are generated only from
            your indexed documents.

          </p>

        </div>


      </main>

    </div>
  );
}


export default App;