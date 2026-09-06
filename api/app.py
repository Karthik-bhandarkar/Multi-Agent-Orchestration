from fastapi import FastAPI

app = FastAPI(title="EduPulse AI Backend", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "HEALTHY"}
