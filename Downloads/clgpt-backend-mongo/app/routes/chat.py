from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
import openai

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    persona: str
    topic: str

mongo_client = MongoClient(os.environ["MONGO_URI"])
db = mongo_client[os.environ["MONGO_DB"]]
collection = db[os.environ["MONGO_COLLECTION"]]

@router.post("/chat/")
async def chat_endpoint(req: ChatRequest):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.api_base = os.environ["OPENAI_ENDPOINT"]
    openai.api_type = "azure"
    openai.api_version = "2024-02-15-preview"

    messages = [{"role": "system", "content": f"You are {req.persona}"},
                {"role": "user", "content": req.message}]

    completion = openai.ChatCompletion.create(
        deployment_id=os.environ["OPENAI_DEPLOYMENT"],
        messages=messages
    )
    reply = completion.choices[0].message.content

    collection.insert_one({
        "user_id": req.user_id,
        "topic": req.topic,
        "message": req.message,
        "response": reply,
        "timestamp": datetime.utcnow().isoformat()
    })

    return {"response": reply}

@router.post("/save/")
async def save_chat(data: dict):
    collection.insert_one(data)
    return {"status": "saved"}

@router.get("/list/")
async def list_chats(user_id: str):
    topics = collection.distinct("topic", {"user_id": user_id})
    return {"topics": topics}

@router.get("/load/")
async def load_chat(user_id: str, topic: str):
    chats = list(collection.find({"user_id": user_id, "topic": topic}))
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    return {"chats": chats}
