from openai import OpenAI
from dotenv import load_dotenv
import os

print("hello")

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Read OpenAI API Key
# ============================================================

api_key = os.getenv("OPENAI_API_KEY")

# ============================================================
# Create OpenAI Client
# ============================================================

client = OpenAI(api_key=api_key)

# ============================================================
# Function to Call GPT Model
# ============================================================

def ask_gpt(model, input):
    response =  client.responses.create(
            model = model,
            input = input
    )
    print(response)
    return response.output_text
