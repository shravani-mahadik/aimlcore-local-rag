from backend.app.services.generation.llm_service import (
    LLMService
)


print("\n===== OLLAMA LLM TEST =====")


service = LLMService()


prompt = """
Answer this question briefly:

What is 2 + 2?
"""


answer = service.generate(
    prompt
)


print("\n===== ANSWER =====")
print(answer)


print("\n===== SUCCESS =====")