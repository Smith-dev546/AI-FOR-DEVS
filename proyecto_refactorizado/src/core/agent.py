"""
Clase base para agentes del sistema
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..core.llm_client import LLMClient
from ..skills.base_skill import BaseSkill

class BaseAgent(ABC):
    """
    Clase base abstracta para todos los agentes del sistema
    
    Proporciona la estructura fundamental para agentes con habilidades (skills)
    """
    
    def __init__(
        self,
        name: str = "BaseAgent",
        llm_client: Optional[LLMClient] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa el agente base
        
        Args:
            name: Nombre del agente
            llm_client: Cliente LLM (si no se proporciona, crea uno nuevo)
            config: Configuración adicional del agente
        """
        self.name = name
        self.llm_client = llm_client or LLMClient()
        self.config = config or {}
        self.skills: Dict[str, BaseSkill] = {}
        self._system_prompt = None
        
        # Configuración del agente
        self._setup_from_config()
    
    def _setup_from_config(self):
        """Configura el agente desde el diccionario de configuración"""
        self.role = self.config.get("role", "asistente virtual")
        self.style = self.config.get("style", "profesional")
        self.context = self.config.get("context", "")
        self.max_history = self.config.get("max_history", 10)
        self.history = []
    
    @abstractmethod
    def process(self, input_data: Any, **kwargs) -> Any:
        """
        Método principal que debe implementar cada agente
        
        Args:
            input_data: Datos de entrada (puede ser texto, dict, etc.)
            **kwargs: Argumentos adicionales
            
        Returns:
            Resultado del procesamiento
        """
        pass
    
    def add_skill(self, name: str, skill: BaseSkill) -> bool:
        """
        Agrega una skill al agente
        
        Args:
            name: Nombre único de la skill
            skill: Instancia de la skill
            
        Returns:
            True si se agregó correctamente, False si ya existía
        """
        if name in self.skills:
            return False
        
        self.skills[name] = skill
        return True
    
    def remove_skill(self, name: str) -> bool:
        """
        Elimina una skill del agente
        
        Args:
            name: Nombre de la skill
            
        Returns:
            True si se eliminó, False si no existía
        """
        if name not in self.skills:
            return False
        
        del self.skills[name]
        return True
    
    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """
        Obtiene una skill por su nombre
        
        Args:
            name: Nombre de la skill
            
        Returns:
            Instancia de la skill o None si no existe
        """
        return self.skills.get(name)
    
    def list_skills(self) -> Dict[str, str]:
        """
        Lista todas las skills con su descripción
        
        Returns:
            Diccionario {nombre: descripción}
        """
        return {
            name: skill.description 
            for name, skill in self.skills.items()
        }
    
    def execute_skill(self, skill_name: str, **kwargs) -> Any:
        """
        Ejecuta una skill específica
        
        Args:
            skill_name: Nombre de la skill a ejecutar
            **kwargs: Argumentos para la skill
            
        Returns:
            Resultado de la ejecución de la skill
            
        Raises:
            KeyError: Si la skill no existe
        """
        if skill_name not in self.skills:
            raise KeyError(f"Skill '{skill_name}' no encontrada")
        
        skill = self.skills[skill_name]
        return skill.execute(**kwargs)
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        Actualiza la configuración del agente
        
        Args:
            new_config: Diccionario con la nueva configuración
        """
        self.config.update(new_config)
        self._setup_from_config()
    
    def get_config(self) -> Dict[str, Any]:
        """
        Obtiene la configuración actual del agente
        
        Returns:
            Diccionario con la configuración
        """
        return {
            "name": self.name,
            "role": self.role,
            "style": self.style,
            "context": self.context,
            "max_history": self.max_history,
            "skills_count": len(self.skills),
            **self.config
        }
    
    def add_to_history(self, message: Dict[str, Any]):
        """
        Agrega un mensaje al historial del agente
        
        Args:
            message: Mensaje a agregar (debe ser dict con 'role' y 'content')
        """
        self.history.append(message)
        
        # Limitar historial
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def clear_history(self):
        """Limpia el historial del agente"""
        self.history = []
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Obtiene el historial del agente
        
        Returns:
            Lista de mensajes en el historial
        """
        return self.history.copy()
    
    def create_system_prompt(self) -> str:
        """
        Crea el prompt del sistema para el agente
        
        Returns:
            String con el prompt del sistema
        """
        if self.config.get("custom_system_prompt"):
            return self.config["custom_system_prompt"]
        
        return f"""
        Eres {self.name}, un {self.role} con un estilo {self.style}.
        {self.context}
        
        Dispones de las siguientes habilidades (skills):
        {self._format_skills_description()}
        
        Responde de manera clara, concisa y profesional.
        """
    
    def _format_skills_description(self) -> str:
        """Formatea la descripción de las skills"""
        if not self.skills:
            return "  - Ninguna skill disponible"
        
        return "\n".join([
            f"  - {name}: {skill.description}" 
            for name, skill in self.skills.items()
        ])
    
    def __str__(self) -> str:
        return f"Agent(name='{self.name}', skills={len(self.skills)})"
    
    def __repr__(self) -> str:
        return self.__str__()

# Ejemplo de uso:
# class MiAgente(BaseAgent):
#     def process(self, input_data: str, **kwargs) -> str:
#         # Implementación específica
#         return f"Procesado: {input_data}"