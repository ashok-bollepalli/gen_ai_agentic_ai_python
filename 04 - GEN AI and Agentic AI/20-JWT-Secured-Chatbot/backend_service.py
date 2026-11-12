"""
backend_service.py - FastAPI REST API.

  POST /register  -> create user
  POST /login     -> returns JWT token
  POST /chat      -> needs header "Authorization: Bearer <token>"

Run: python backend_service.py   |   Docs: http://localhost:8000/docs
"""
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai import OpenAI
from pydantic import BaseModel

from config import config
from db_service import init_db, login_user, register_user
from jwt_service import create_token, validate_token

init_db()  # create DB + users table if missing
app = FastAPI(title="Gen AI Chatbot API")
llm = OpenAI(api_key=config.OPENAI_API_KEY)


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(LoginRequest):
    email: str


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []  # [{"role": "user" | "assistant", "content": "..."}]


def current_user(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Runs before /chat: validates the Bearer token, returns the username."""
    username = validate_token(auth.credentials)
    if not username:
        raise HTTPException(401, "Invalid or expired token")
    return username


@app.post("/register")
def register(req: RegisterRequest):
    if not req.username or not req.password:
        raise HTTPException(400, "Username and password are required")
    if not register_user(req.username, req.email, req.password):
        raise HTTPException(409, "Username or email already exists")
    return {"message": "User registered successfully"}


@app.post("/login")
def login(req: LoginRequest):
    if not login_user(req.username, req.password):
        raise HTTPException(401, "Invalid username or password")
    return {"access_token": create_token(req.username), "token_type": "bearer", "username": req.username}


@app.post("/chat")
def chat(req: ChatRequest, username: str = Depends(current_user)):
    messages = [{"role": "system", "content": "You are a helpful AI assistant."},
                *req.history,
                {"role": "user", "content": req.message}]
    response = llm.chat.completions.create(model=config.OPENAI_MODEL, messages=messages)
    return {"reply": response.choices[0].message.content, "user": username}


if __name__ == "__main__":
    uvicorn.run("backend_service:app", host=config.BACKEND_HOST, port=config.BACKEND_PORT, reload=True)