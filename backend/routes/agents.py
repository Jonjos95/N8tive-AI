"""
Agent management endpoints (CRUD operations).
All routes require a valid N8tive Portal JWT — agents are scoped per user.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from utils.memory_manager import MemoryManager
from middleware.auth import get_current_user

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
async def list_agents(current_user: dict = Depends(get_current_user)):
    """List all agents owned by the authenticated user."""
    try:
        agents = memory_manager.list_agents(user_id=current_user["sub"])
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific agent (must be owned by the authenticated user)."""
    try:
        agent = memory_manager.get_agent(agent_id, user_id=current_user["sub"])
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents")
async def create_agent(agent: AgentCreate, current_user: dict = Depends(get_current_user)):
    """Create a new agent owned by the authenticated user."""
    try:
        agent_id = memory_manager.create_agent(
            name=agent.name,
            role=agent.role,
            system_prompt=agent.system_prompt,
            tone=agent.tone,
            temperature=agent.temperature,
            model=agent.model,
            user_id=current_user["sub"],
        )
        return {"agent_id": agent_id, "message": "Agent created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/agents/{agent_id}")
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update an agent (must be owned by the authenticated user)."""
    try:
        # Ownership check
        if not memory_manager.get_agent(agent_id, user_id=current_user["sub"]):
            raise HTTPException(status_code=404, detail="Agent not found")
        updated = memory_manager.update_agent(agent_id, agent_update.dict(exclude_none=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an agent and its chat history (must be owned by the authenticated user)."""
    try:
        if not memory_manager.get_agent(agent_id, user_id=current_user["sub"]):
            raise HTTPException(status_code=404, detail="Agent not found")
        deleted = memory_manager.delete_agent(agent_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/history")
async def get_chat_history(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Get chat history for an agent (must be owned by the authenticated user)."""
    try:
        if not memory_manager.get_agent(agent_id, user_id=current_user["sub"]):
            raise HTTPException(status_code=404, detail="Agent not found")
        history = memory_manager.get_chat_history(agent_id)
        return {"agent_id": agent_id, "history": history}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}/history")
async def clear_chat_history(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Clear chat history for an agent (must be owned by the authenticated user)."""
    try:
        if not memory_manager.get_agent(agent_id, user_id=current_user["sub"]):
            raise HTTPException(status_code=404, detail="Agent not found")
        memory_manager.clear_chat_history(agent_id)
        return {"message": "Chat history cleared successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
