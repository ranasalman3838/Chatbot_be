from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

chat_router = APIRouter()

async def generate_response(query: str):
    """
    Simulates a chatbot streaming response by sending chunks of text.
    """
    response = f"Processing your query: {query}\n"
    for word in response.split():
        yield word + " "
        await asyncio.sleep(0.2)  # Simulating delay for streaming effect

@chat_router.get("/chat")
async def chatbot(query: str):
    """
    Chatbot endpoint that streams responses based on the input query.
    """
    return StreamingResponse(generate_response(query), media_type="text/plain")