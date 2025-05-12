from fastapi import FastAPI
from app.router import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Safety‑First Triage API")
app.include_router(router)

@app.get("/")
def root(): return {"status":"ok"}
