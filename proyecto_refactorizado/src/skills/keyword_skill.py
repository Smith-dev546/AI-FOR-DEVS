from typing import Dict, Any, List
from .base_skill import BaseSkill

class KeywordSkill(BaseSkill):
    """Skill para extraer palabras clave"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Extrae las palabras clave de un texto"
        self.default_n = 5
    
    def execute(self, texto: str, n: int = 5, **kwargs) -> Dict[str, Any]:
        """Ejecuta extracción de palabras clave"""
        if not texto:
            return {"error": "El texto no puede estar vacío"}
        
        variables = {
            "texto": texto,
            "n": n
        }
        
        try:
            resultado = self.llm_client.generate(
                prompt_key="keywords",
                variables=variables
            )
            
            # Procesar resultado (puede ser lista separada por comas)
            palabras = [p.strip() for p in resultado.split(",")]
            
            return {
                "palabras_clave": palabras[:n],
                "texto_original": texto,
                "cantidad": len(palabras)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_input_schema(self) -> Dict:
        return {
            "texto": {"type": "string", "required": True, "description": "Texto para extraer keywords"},
            "n": {"type": "integer", "required": False, "description": "Número de palabras", "default": 5}
        }