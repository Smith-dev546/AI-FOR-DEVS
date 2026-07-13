from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..core.llm_client import LLMClient

class BaseSkill(ABC):
    """Interfaz base para todas las skills"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self.name = self.__class__.__name__
        self.description = "Skill base"
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Método principal de ejecución de la skill"""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Retorna metadata de la skill"""
        return {
            "name": self.name,
            "description": self.description,
            "inputs": self._get_input_schema(),
            "outputs": self._get_output_schema()
        }
    
    def _get_input_schema(self) -> Dict:
        """Define el esquema de entrada (sobrescribir si es necesario)"""
        return {}
    
    def _get_output_schema(self) -> Dict:
        """Define el esquema de salida (sobrescribir si es necesario)"""
        return {}