import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2:3b"


class LLMService:
    """
    Local LLM service using Ollama.
    """

    def __init__(
        self,
        model: str = MODEL_NAME
    ):
        self.model = model

    def generate(
        self,
        prompt: str
    ) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()

def build_grounded_prompt(
    question: str,
    context: str
) -> str:

    return f"""
You are AIMLCore Local Knowledge Assistant.

Answer the user's question using ONLY the information in the CONTEXT.

STRICT RULES:

1. Find the answer directly from the provided context.
2. Do not use outside knowledge.
3. Do not guess or assume.
4. Give ONLY the final answer to the user's question.
5. Do NOT repeat the context.
6. Do NOT output SOURCE, Document, Page, Chunk, Similarity, or Content.
7. Do NOT output the retrieved text.
8. Do NOT explain your reasoning.
9. Do NOT write "According to the provided context".
10. Do NOT write "Answer:" before the answer.
11. Do NOT include citations in your response. The application will display
    the source information separately.
12. If the answer is explicitly present in the context, answer it directly.
13. If the answer cannot be found in the context, respond exactly:

I could not find enough information in the uploaded knowledge base.

Examples:

Question: What position was I offered?

Good answer:
You were offered the position of AI/ML Engineer at AIMLCore.

Bad answer:
[Source: sample_document_001, Page: 1]
Chunk: sample_document_001_chunk_0
Similarity: 0.3330
Content: ...
Answer: AI/ML Engineer

Question: What was the start date?

Good answer:
The start date was July 13, 2026.

Bad answer:
Content: Start Date: July 13, 2026
Answer: July 13, 2026

================ CONTEXT ================

{context}

================ QUESTION ================

{question}

================ FINAL ANSWER ================
""".strip()
