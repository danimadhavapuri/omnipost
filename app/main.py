from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import post_to_all_platforms
import webbrowser
import threading

app = FastAPI(
    title="OmniPost — Automated Multi-Platform Posting System",
    description="Automatically post your message to 5+ platforms with one API call.",
    version="1.0.0"
)


def open_browser():
    webbrowser.open("http://localhost:4000/docs")


@app.on_event("startup")
async def startup_event():
    threading.Timer(1.5, open_browser).start()


@app.get("/", tags=["Health"])
def home():
    """Check if the server is running."""
    return {
        "app": "OmniPost",
        "description": "Automated Multi-Platform Posting System",
        "docs": "http://localhost:4000/docs",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/posting", response_model=PostingResponse, tags=["Posting"])
def post_message(request: PostingRequest):
    """
    Post a message to all configured platforms automatically.

    Rules:
    - Message must be **max 200 characters**
    - Message must contain **exactly 1 valid URL**
    """
    results = post_to_all_platforms(request.message)

    successful = [r for r in results if r.status == "success"]
    failed = [r for r in results if r.status == "failed"]

    return PostingResponse(
        success=len(failed) == 0,
        total_platforms=len(results),
        successful=len(successful),
        failed=len(failed),
        results=results
    )