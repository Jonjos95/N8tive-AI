"""
Memory manager for agents and chat history
Uses SQLite for persistent storage (with JSON fallback option)
"""

import json
import os
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class MemoryManager:
    def __init__(self, db_path: str = "data/agents.db", json_path: str = "data/agents.json"):
        self.db_path = db_path
        self.json_path = json_path
        self.use_db = os.getenv("USE_DATABASE", "true").lower() == "true"
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        if self.use_db:
            self._init_database()
        else:
            self._init_json_storage()
    
    def _init_database(self):
        """Initialize SQLite database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                system_prompt TEXT NOT NULL,
                tone TEXT DEFAULT 'professional',
                temperature REAL DEFAULT 0.7,
                model TEXT DEFAULT 'gpt-3.5-turbo',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Add user_id column to existing databases that predate this migration
        try:
            cursor.execute("ALTER TABLE agents ADD COLUMN user_id TEXT")
        except Exception:
            pass  # Column already exists
        
        # Chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _init_json_storage(self):
        """Initialize JSON storage file if it doesn't exist"""
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as f:
                json.dump({"agents": {}, "chat_history": {}}, f)
    
    def list_agents(self, user_id: Optional[str] = None) -> List[Dict]:
        """List agents, optionally scoped to a user."""
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if user_id:
                cursor.execute(
                    "SELECT * FROM agents WHERE user_id = ? ORDER BY created_at DESC",
                    (user_id,)
                )
            else:
                cursor.execute("SELECT * FROM agents ORDER BY created_at DESC")
            rows = cursor.fetchall()
            agents = [dict(row) for row in rows]
            conn.close()
            return agents
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            agents = list(data["agents"].values())
            if user_id:
                agents = [a for a in agents if a.get("user_id") == user_id]
            return agents
    
    def get_agent(self, agent_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        """Get a specific agent, optionally enforcing user ownership."""
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if user_id:
                cursor.execute(
                    "SELECT * FROM agents WHERE id = ? AND user_id = ?",
                    (agent_id, user_id)
                )
            else:
                cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            agent = data["agents"].get(agent_id)
            if agent and user_id and agent.get("user_id") != user_id:
                return None
            return agent
    
    def create_agent(
        self,
        name: str,
        role: str,
        system_prompt: str,
        tone: str = "professional",
        temperature: float = 0.7,
        model: str = "gpt-3.5-turbo",
        user_id: Optional[str] = None,
    ) -> str:
        """Create a new agent owned by user_id."""
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agents (id, user_id, name, role, system_prompt, tone, temperature, model, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (agent_id, user_id, name, role, system_prompt, tone, temperature, model, now, now))
            conn.commit()
            conn.close()
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)

            data["agents"][agent_id] = {
                "id": agent_id,
                "user_id": user_id,
                "name": name,
                "role": role,
                "system_prompt": system_prompt,
                "tone": tone,
                "temperature": temperature,
                "model": model,
                "created_at": now,
                "updated_at": now
            }

            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=2)

        return agent_id
    
    def update_agent(self, agent_id: str, updates: Dict) -> bool:
        """Update an existing agent"""
        if not self.get_agent(agent_id):
            return False
        
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [agent_id]
            
            cursor.execute(f"UPDATE agents SET {set_clause} WHERE id = ?", values)
            conn.commit()
            conn.close()
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            
            if agent_id in data["agents"]:
                data["agents"][agent_id].update(updates)
                
                with open(self.json_path, "w") as f:
                    json.dump(data, f, indent=2)
        
        return True
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent and its chat history"""
        if not self.get_agent(agent_id):
            return False
        
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE agent_id = ?", (agent_id,))
            cursor.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
            conn.commit()
            conn.close()
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            
            if agent_id in data["agents"]:
                del data["agents"][agent_id]
            
            if agent_id in data["chat_history"]:
                del data["chat_history"][agent_id]
            
            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=2)
        
        return True
    
    def get_chat_history(self, agent_id: str) -> List[Dict]:
        """Get chat history for an agent"""
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content, timestamp
                FROM chat_history
                WHERE agent_id = ?
                ORDER BY timestamp ASC
            """, (agent_id,))
            rows = cursor.fetchall()
            history = [{"role": row["role"], "content": row["content"]} for row in rows]
            conn.close()
            return history
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            return data["chat_history"].get(agent_id, [])
    
    def add_message(self, agent_id: str, role: str, content: str):
        """Add a message to chat history"""
        timestamp = datetime.utcnow().isoformat()
        
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history (agent_id, role, content, timestamp)
                VALUES (?, ?, ?, ?)
            """, (agent_id, role, content, timestamp))
            conn.commit()
            conn.close()
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            
            if agent_id not in data["chat_history"]:
                data["chat_history"][agent_id] = []
            
            data["chat_history"][agent_id].append({
                "role": role,
                "content": content,
                "timestamp": timestamp
            })
            
            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=2)
    
    def clear_chat_history(self, agent_id: str):
        """Clear chat history for an agent"""
        if self.use_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE agent_id = ?", (agent_id,))
            conn.commit()
            conn.close()
        else:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            
            if agent_id in data["chat_history"]:
                data["chat_history"][agent_id] = []
            
            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=2)







