from typing import Dict, Any, Optional, List
from ..core.llm_client import LLMClient
from ..skills.sentiment_skill import SentimentSkill
from ..skills.summarizer_skill import SummarizerSkill
from ..skills.keyword_skill import KeywordSkill

class TextAnalystAgent:
    """Agente personalizado para análisis de texto con múltiples skills"""
    
    def __init__(
        self,
        name: str = "Analista de Texto",
        llm_client: Optional[LLMClient] = None,
        config: Optional[Dict] = None
    ):
        self.name = name
        self.llm_client = llm_client or LLMClient()  # Ya maneja modo mock
        self.config = config or self._default_config()
        
        # Inicializar skills con el mismo cliente
        self.skills = {
            "sentiment": SentimentSkill(llm_client=self.llm_client),
            "summarizer": SummarizerSkill(llm_client=self.llm_client),
            "keywords": KeywordSkill(llm_client=self.llm_client)
        }
        
        # Configuración del agente
        self.role = self.config.get("role", "asistente de análisis textual")
        self.style = self.config.get("style", "profesional y objetivo")
        self.context = self.config.get("context", "")
        
        # Registrar personalización
        self._setup_personalization()
    
    def _default_config(self) -> Dict:
        return {
            "role": "asistente de análisis textual",
            "style": "profesional y objetivo",
            "context": "",
            "max_tokens": 500,
            "temperature": 0.7
        }
    
    def _setup_personalization(self):
        """Configura la personalización del agente"""
        if self.config.get("custom_system_prompt"):
            self.system_prompt = self.config["custom_system_prompt"]
        else:
            self.system_prompt = f"""
            Eres un {self.role} con un estilo {self.style}.
            {self.context}
            
            Tus respuestas deben ser claras, precisas y útiles para el usuario.
            Utiliza las skills disponibles para analizar textos de manera profesional.
            """
    
    def analyze_text(self, texto: str, skills: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analiza un texto usando las skills solicitadas"""
        if not texto:
            return {"error": "El texto no puede estar vacío"}
        
        if skills is None:
            skills = list(self.skills.keys())
        
        resultados = {
            "texto": texto,
            "longitud": len(texto.split()),
            "analisis": {}
        }
        
        for skill_name in skills:
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                
                try:
                    if skill_name == "sentiment":
                        resultado = skill.execute(texto=texto)
                    elif skill_name == "summarizer":
                        resultado = skill.execute(
                            texto=texto,
                            max_palabras=self.config.get("summary_length", 100)
                        )
                    elif skill_name == "keywords":
                        resultado = skill.execute(
                            texto=texto,
                            n=self.config.get("keywords_count", 5)
                        )
                    else:
                        continue
                    
                    resultados["analisis"][skill_name] = resultado
                except Exception as e:
                    resultados["analisis"][skill_name] = {"error": str(e)}
        
        # Análisis combinado
        if self.config.get("enable_combined_analysis", True):
            try:
                resultados["analisis_combinado"] = self._generate_combined_analysis(
                    texto, 
                    resultados["analisis"]
                )
            except Exception as e:
                resultados["analisis_combinado"] = f"Error en análisis combinado: {e}"
        
        return resultados
    
    def _generate_combined_analysis(self, texto: str, analisis: Dict) -> str:
        """Genera un análisis combinado usando el LLM"""
        resumen = f"Texto: {texto[:100]}...\n\nAnálisis:\n"
        for skill, resultado in analisis.items():
            if isinstance(resultado, dict):
                for key, value in resultado.items():
                    if key != "texto_original":
                        resumen += f"- {skill}.{key}: {value}\n"
        
        variables = {
            "texto": texto,
            "analisis": resumen
        }
        
        try:
            analysis = self.llm_client.generate(
                prompt_key="combined_analysis",
                variables=variables,
                system_prompt=self.system_prompt
            )
            return analysis.strip()
        except Exception as e:
            return f"Error en análisis combinado: {str(e)}"
    
    def list_skills(self) -> Dict[str, str]:
        """Lista las skills disponibles"""
        return {
            name: skill.description 
            for name, skill in self.skills.items()
        }
    
    def add_skill(self, name: str, skill: Any):
        """Agrega una nueva skill al agente"""
        self.skills[name] = skill
    
    def get_config(self) -> Dict:
        """Retorna la configuración actual del agente"""
        return {
            "name": self.name,
            "role": self.role,
            "style": self.style,
            "context": self.context,
            **self.config
        }
    
    def update_config(self, new_config: Dict):
        """Actualiza la configuración del agente"""
        self.config.update(new_config)
        self._setup_personalization()