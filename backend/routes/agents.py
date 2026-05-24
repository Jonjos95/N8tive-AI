"""
Agent management endpoints (CRUD operations)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from utils.memory_manager import MemoryManager

router = APIRouter()
memory_manager = MemoryManager()

class AgentCreate(BaseModel):
    name: str
    role: str
    system_prompt: str
    tone: str = "professional"
    temperature: float = 0.7
    model: str = "gpt-3.5-turbo"

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    system_prompt: Optional[str] = None
    tone: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None

@router.get("/agents")
async def list_agents():
    """Get all agents"""
    try:
        agents = memory_manager.list_agents()
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    try:
        agent = memory_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents")
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    try:
        agent_id = memory_manager.create_agent(
            name=agent.name,
            role=agent.role,
            system_prompt=agent.system_prompt,
            tone=agent.tone,
            temperature=agent.temperature,
            model=agent.model
        )
        return {"agent_id": agent_id, "message": "Agent created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/agents/{agent_id}")
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update an existing agent"""
    try:
        updated = memory_manager.update_agent(agent_id, agent_update.dict(exclude_none=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent and its chat history"""
    try:
        deleted = memory_manager.delete_agent(agent_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_id}/history")
async def get_chat_history(agent_id: str):
    """Get chat history for a specific agent"""
    try:
        history = memory_manager.get_chat_history(agent_id)
        return {"agent_id": agent_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/{agent_id}/history")
async def clear_chat_history(agent_id: str):
    """Clear chat history for a specific agent"""
    try:
        memory_manager.clear_chat_history(agent_id)
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







