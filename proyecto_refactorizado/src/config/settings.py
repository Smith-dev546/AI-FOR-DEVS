"""
Configuración centralizada del sistema agentico
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class LLMConfig:
    """Configuración del cliente LLM"""
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = 500
    api_key: Optional[str] = None
    timeout: int = 60
    
    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Crea configuración desde variables de entorno"""
        return cls(
            model=os.getenv("MODEL", "gpt-3.5-turbo"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "500")) if os.getenv("MAX_TOKENS") else None,
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=int(os.getenv("TIMEOUT", "60"))
        )

@dataclass
class AgentConfig:
    """Configuración del agente"""
    name: str = "Agente Base"
    role: str = "asistente de análisis"
    style: str = "profesional y objetivo"
    context: str = ""
    temperature: float = 0.7
    max_tokens: int = 500
    enable_combined_analysis: bool = True
    summary_length: int = 100
    keywords_count: int = 5
    custom_system_prompt: Optional[str] = None
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "AgentConfig":
        """Crea configuración desde diccionario"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            "name": self.name,
            "role": self.role,
            "style": self.style,
            "context": self.context,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "enable_combined_analysis": self.enable_combined_analysis,
            "summary_length": self.summary_length,
            "keywords_count": self.keywords_count,
            "custom_system_prompt": self.custom_system_prompt
        }

@dataclass
class SkillsConfig:
    """Configuración de skills"""
    enabled_skills: list = field(default_factory=lambda: ["sentiment", "summarizer", "keywords"])
    language: str = "es"
    confidence_threshold: float = 0.7
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "SkillsConfig":
        """Crea configuración desde diccionario"""
        return cls(**config_dict)

class Settings:
    """Configuración global del sistema"""
    
    def __init__(self):
        self.llm = LLMConfig.from_env()
        self.agent = AgentConfig()
        self.skills = SkillsConfig()
        self.base_dir = Path(__file__).parent.parent.parent
        self.prompts_path = self.base_dir / "prompts" / "prompts.yaml"
        self.logs_dir = self.base_dir / "logs"
        
        # Crear directorios necesarios
        self._create_directories()
    
    def _create_directories(self):
        """Crea directorios necesarios si no existen"""
        self.logs_dir.mkdir(exist_ok=True)
        
    def update_llm_config(self, **kwargs):
        """Actualiza configuración del LLM"""
        for key, value in kwargs.items():
            if hasattr(self.llm, key):
                setattr(self.llm, key, value)
    
    def update_agent_config(self, **kwargs):
        """Actualiza configuración del agente"""
        for key, value in kwargs.items():
            if hasattr(self.agent, key):
                setattr(self.agent, key, value)
    
    def update_skills_config(self, **kwargs):
        """Actualiza configuración de skills"""
        for key, value in kwargs.items():
            if hasattr(self.skills, key):
                setattr(self.skills, key, value)
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Retorna resumen de configuración"""
        return {
            "llm": {
                "model": self.llm.model,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens
            },
            "agent": self.agent.to_dict(),
            "skills": {
                "enabled": self.skills.enabled_skills,
                "language": self.skills.language
            }
        }

# Instancia global de configuración
settings = Settings()

def get_settings() -> Settings:
    """Obtiene la instancia global de configuración"""
    return settings

def reset_settings():
    """Reinicia la configuración a valores por defecto"""
    global settings
    settings = Settings()

# Ejemplo de uso:
# from src.config.settings import settings, get_settings
# config = get_settings()
# print(config.llm.model)