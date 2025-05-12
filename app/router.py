from fastapi import APIRouter
from pydantic import BaseModel
from app.model import RiskModel
from app.rag import Retriever
import app.prompt as prompts
import os
from openai import OpenAI
import streamlit as st

openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]
router = APIRouter()
risk_model = RiskModel(os.getenv("MODEL_DIR"))
retriever  = Retriever()

openai_client = OpenAI(api_key=openai_api_key)

class TextIn(BaseModel):
    text:str

@router.post("/predict")
def predict(user_text: TextIn):
    risk_score, confidence, _ = risk_model.score(user_text.text)
    return {"risk_score": risk_score, "confidence": confidence}

@router.post("/advise")
def advise(inp: TextIn):
    risk_score, confidence, _ = risk_model.score(inp.text)
    snippets = retriever.get(inp.text, k=3)
    prompt = prompts.build_prompt(inp.text, risk_score, confidence, snippets)

    response = openai_client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "system", "content": prompts.get_system_prompt()},
            {"role":"user","content":prompt}
            ],
        max_tokens=1024,
        temperature=0.1
    ).choices[0].message.content

    return {
        "risk": {"risk score": risk_score, "confidence": round(confidence,4)},
        "advice": response,
        "snippets": snippets
    }
