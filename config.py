import os
from typing import Dict, Any
from uuid import UUID
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Discord
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    GUILD_ID: int = int(os.getenv("GUILD_ID", "0"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Encryption
    VAULT_KEY_ID: str = os.getenv("VAULT_KEY_ID", "aca-master-key")
    
    # Project Config (pre-seeded for core Arcium project)
    PROJECTS: Dict[str, Dict[str, Any]] = {
        "arcium": {
            "project_id": UUID("00000000-0000-0000-0000-000000000001"),
            "root_nodes": {"explorer": 1, "builder": 101, "guardian": 201}
        }
    }
    
    def get_project_id(self, slug: str) -> UUID:
        return self.PROJECTS[slug]["project_id"]
    
    def get_root_node_id(self, slug: str, path: str) -> int:
        return self.PROJECTS[slug]["root_nodes"][path]

settings = Settings()