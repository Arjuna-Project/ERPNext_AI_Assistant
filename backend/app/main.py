from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_response
from dotenv import load_dotenv
import os

# 1. Load environment variables from your .env file
load_dotenv()

app = FastAPI(title="ERP AI Assistant Backend")

# 2. CONFIGURE CORS
# This allows your frontend (index.html) to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; fine for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 3. CHAT ENDPOINT
@app.get("/chat")
async def chat(query: str):
    """
    Receives the query from the frontend and returns the AI-processed 
    response from the ERP system.
    """
    try:
        # Call the get_response function from chatbot.py
        response_text = get_response(query)
        return {"response": response_text}
    except Exception as e:
        # Catch-all for unexpected backend errors
        return {"response": f"⚠️ Backend Error: {str(e)}"}

# 4. HEALTH CHECK (Optional)
@app.get("/")
def read_root():
    return {"message": "ERP AI Chatbot Server is Live!"}
