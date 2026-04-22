from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_response
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="ERP AI Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
async def chat(query: str):
    try:
        # Call the get_response function from chatbot.py
        response_text = get_response(query)
        return {"response": response_text}
    except HTTPException:
        raise
    except Exception as e:
        # Catch backend errors
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "ERP AI Chatbot Server is Live!"}
