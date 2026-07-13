from typing import Dict, Any
from .base_skill import BaseSkill

class SummarizerSkill(BaseSkill):
    """Skill para resumir textos"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Genera un resumen conciso de un texto"
        self.max_words = 100
    
    def execute(self, texto: str, max_palabras: int = 100, **kwargs) -> Dict[str, Any]:
        """Ejecuta resumen del texto"""
        if not texto:
            return {"error": "El texto no puede estar vacío"}
        
        self.max_words = max_palabras
        
        variables = {
            "texto": texto,
            "max_palabras": max_palabras
        }
        
        try:
            resumen = self.llm_client.generate(
                prompt_key="summarizer",
                variables=variables
            )
            
            return {
                "resumen": resumen.strip(),
                "texto_original": texto,
                "palabras_original": len(texto.split()),
                "palabras_resumen": len(resumen.split())
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_input_schema(self) -> Dict:
        return {
            "texto": {"type": "string", "required": True, "description": "Texto a resumir"},
            "max_palabras": {"type": "integer", "required": False, "description": "Máximo de palabras", "default": 100}
        }