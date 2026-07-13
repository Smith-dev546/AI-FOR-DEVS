from typing import Dict, Any
from .base_skill import BaseSkill

class SentimentSkill(BaseSkill):
    """Skill para análisis de sentimiento"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Analiza el sentimiento de un texto (positivo/negativo/neutral)"
        self.language = "es"
    
    def execute(self, texto: str, **kwargs) -> Dict[str, Any]:
        """Ejecuta análisis de sentimiento"""
        if not texto:
            return {"error": "El texto no puede estar vacío"}
        
        # Si el texto es muy corto, ajustamos el prompt
        if len(texto.split()) < 5:
            prompt_key = "sentiment_short"
        else:
            prompt_key = "sentiment"
        
        variables = {
            "texto": texto,
            "idioma": self.language
        }
        
        try:
            resultado = self.llm_client.generate(
                prompt_key=prompt_key,
                variables=variables
            )
            
            # Limpiar y estructurar respuesta
            sentimiento = resultado.strip().lower()
            if "positivo" in sentimiento:
                sentimiento = "positivo"
            elif "negativo" in sentimiento:
                sentimiento = "negativo"
            else:
                sentimiento = "neutral"
            
            return {
                "sentimiento": sentimiento,
                "texto_original": texto,
                "confianza": self._calcular_confianza(sentimiento)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _calcular_confianza(self, sentimiento: str) -> float:
        """Calcula un nivel de confianza base (mejorable con más lógica)"""
        if sentimiento == "positivo":
            return 0.85
        elif sentimiento == "negativo":
            return 0.82
        else:
            return 0.70
    
    def _get_input_schema(self) -> Dict:
        return {
            "texto": {"type": "string", "required": True, "description": "Texto a analizar"}
        }