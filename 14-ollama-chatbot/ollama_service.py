import ollama

MODEL_NAME = "llama3.2:latest"

def ask_ollama(question):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response["message"]["content"]
