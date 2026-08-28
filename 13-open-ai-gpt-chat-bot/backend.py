from dotenv import load_dotenv
from openai import OpenAI
import os
from fastapi import FastAPI
from pydantic import BaseModel

#load envrionment variable from .env file
load_dotenv()


# create Open AI client for communication
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

# Create FAST API Application
app = FastAPI(
    title = "GEN AI Backend API",
    description = "Backend API to access OPEN AI GPT Model",
    version = "1.0.0"
)

# Request DTO / Model
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message" : "GEN AI Backend API is running successfully"
    }

@app.post("/ask-ai")
def ask_ai(request: QuestionRequest):
    response = client.responses.create(
        model = "gpt-5.5",
        input = request.question,
        instructions = "You are a helpful AI assistant, Answer clearly and simply",
        max_output_tokens = 500
    )

    return {
        "question" : request.question,
        "answer" : response.output_text
    }


