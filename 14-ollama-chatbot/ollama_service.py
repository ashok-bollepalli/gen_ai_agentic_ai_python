import ollama

MODEL_NAME="llama3.2"

def ask_ollama(message):

    """
        Send given message to ollama modela and generate ai response
    """

    response = ollama.chat(
        model = MODEL_NAME,
        messages= message
    )

    return response["message"]["content"]