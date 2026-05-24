"""
Chat endpoint for streaming AI responses
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
from utils.model_handler import ModelHandler
from utils.memory_manager import MemoryManager

router = APIRouter()
model_handler = ModelHandler()
memory_manager = MemoryManager()

class ChatRequest(BaseModel):
    agent_id: str
    message: str
    stream: bool = True

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that streams responses from the configured AI model.
    Accepts agent_id and message, injects agent's system prompt, and streams tokens.
    """
    try:
        # Get agent configuration
        agent = memory_manager.get_agent(request.agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Get system prompt and settings
        system_prompt = agent.get("system_prompt", "You are a helpful AI assistant.")
        temperature = agent.get("temperature", 0.7)
        model = agent.get("model", "gpt-3.5-turbo")
        
        # Get conversation history (do NOT add user message yet — only persist after success)
        history = memory_manager.get_chat_history(request.agent_id)

        if request.stream:
            # Stream response
            async def generate_response():
                full_response = ""
                async for chunk in model_handler.stream_chat(
                    messages=history + [{"role": "user", "content": request.message}],
                    system_prompt=system_prompt,
                    temperature=temperature,
                    model=model
                ):
                    if chunk:
                        full_response += chunk
                        yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"

                # Save both sides of the conversation only after a complete response
                memory_manager.add_message(request.agent_id, "user", request.message)
                memory_manager.add_message(request.agent_id, "assistant", full_response)

                # Send final done signal
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            
            return StreamingResponse(
                generate_response(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Non-streaming response
            response = await model_handler.chat(
                messages=history + [{"role": "user", "content": request.message}],
                system_prompt=system_prompt,
                temperature=temperature,
                model=model
            )

            # Save both messages only after a successful response
            memory_manager.add_message(request.agent_id, "user", request.message)
            memory_manager.add_message(request.agent_id, "assistant", response)

            return {"response": response, "agent_id": request.agent_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







