"""
Configuration endpoint for available models and settings
"""

from fastapi import APIRouter
from typing import Dict, List

router = APIRouter()

@router.get("/config")
async def get_config():
    """
    Return available models, default settings, and configuration options
    """
    return {
        "models": [
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "provider": "openai",
                "max_tokens": 4096
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "provider": "openai",
                "max_tokens": 8192
            },
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "provider": "openai",
                "max_tokens": 128000
            },
            {
                "id": "claude-3-opus",
                "name": "Claude 3 Opus",
                "provider": "anthropic",
                "max_tokens": 200000
            },
            {
                "id": "claude-3-sonnet",
                "name": "Claude 3 Sonnet",
                "provider": "anthropic",
                "max_tokens": 200000
            },
            {
                "id": "llama-3-70b",
                "name": "Llama 3 70B",
                "provider": "meta",
                "max_tokens": 8192
            }
        ],
        "default_settings": {
            "temperature": {
                "min": 0.0,
                "max": 2.0,
                "default": 0.7,
                "step": 0.1
            },
            "tones": [
                "professional",
                "casual",
                "friendly",
                "formal",
                "creative",
                "technical",
                "empathetic",
                "humorous"
            ]
        },
        "features": {
            "streaming": True,
            "multi_agent": True,
            "export_formats": ["txt", "json"],
            "memory_persistence": True
        }
    }







