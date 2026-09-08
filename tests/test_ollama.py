from backend.app.services.generation.llm_service import OllamaLLM


print("\n===== OLLAMA CONNECTION TEST =====")


llm = OllamaLLM(
    model="llama3.2:3b"
)


prompt = """
Answer the following question in one sentence.

Question:
What is 2 + 2?
"""


answer = llm.generate(prompt)


print("\n===== MODEL RESPONSE =====")
print(answer)

print("\n===== SUCCESS =====")