"""
Model handler for OpenAI-compatible API calls
Supports streaming and non-streaming responses
Expandable to other providers (Claude, Llama, etc.)
"""

import os
from openai import OpenAI, AsyncOpenAI
from typing import List, Dict, AsyncGenerator, Optional
from dotenv import load_dotenv

load_dotenv()

class ModelHandler:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.hf_api_key = os.getenv("HF_API_KEY")
        
        if self.openai_api_key:
            self.client = AsyncOpenAI(api_key=self.openai_api_key)
        else:
            self.client = None
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
        model: str = "gpt-3.5-turbo"
    ) -> str:
        """
        Non-streaming chat completion
        """
        if not self.client:
            raise Exception("OpenAI API key not configured")
        
        try:
            # Prepare messages with system prompt
            formatted_messages = [{"role": "system", "content": system_prompt}]
            formatted_messages.extend(messages)
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
    
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
        model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:
        """
        Streaming chat completion
        Yields tokens as they are generated
        """
        if not self.client:
            raise Exception("OpenAI API key not configured")
        
        try:
            # Prepare messages with system prompt
            formatted_messages = [{"role": "system", "content": system_prompt}]
            formatted_messages.extend(messages)
            
            stream = await self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield delta.content
        
        except Exception as e:
            raise Exception(f"Error in streaming chat completion: {str(e)}")
    
    def _get_provider(self, model: str) -> str:
        """
        Determine provider based on model name
        """
        if model.startswith("gpt"):
            return "openai"
        elif model.startswith("claude"):
            return "anthropic"
        elif model.startswith("llama"):
            return "meta"
        else:
            return "openai"  # Default

