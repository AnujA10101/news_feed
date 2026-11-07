from fastapi import FastAPI
from news_fetcher import fetch_articles

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

