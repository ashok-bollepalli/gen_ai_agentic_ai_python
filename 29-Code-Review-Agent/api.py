from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import review_code
from review_tools import validate_source

app = FastAPI(
    title="AI Code Review Agent",
    description="LLM-assisted Python code review, static checks and pytest suggestions.",
    version="1.0.0",
)


class ReviewRequest(BaseModel):
    source_code: str = Field(min_length=1, max_length=40000)


@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/review")
def review(request: ReviewRequest):
    try:
        validate_source(request.source_code)
        return review_code(request.source_code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception:
        # Log detailed exceptions on the server in a real deployment.
        raise HTTPException(status_code=500, detail="Review failed. Check server logs.")
