from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

from app.graph.graph_model import GraphModel

chat_router = APIRouter()

async def generate_response(query: str):
    """
    Simulates a chatbot streaming response by sending chunks of text.
    """
    # response = f"Processing your query: {query}\n"
    for word in query.split():
        yield word + " "
        await asyncio.sleep(0.2)  # Simulating delay for streaming effect

@chat_router.get("/chat")
async def chatbot(query: str):
    """
    Chatbot endpoint that streams responses based on the input query.
    """

    workflow = GraphModel().graph_builder.compile()
    state_input = {"text": query}
    result = workflow.invoke(state_input)



    result_final = result["summary"]
    return StreamingResponse(generate_response(result_final), media_type="text/plain")