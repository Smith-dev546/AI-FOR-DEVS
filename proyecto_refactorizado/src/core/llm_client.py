import os
from typing import Optional, List, Dict, Any
from pathlib import Path
import yaml

class LLMClient:
    """Cliente LLM configurable con soporte para múltiples modelos"""
    
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None,
        mock_mode: bool = False
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Verificar si hay API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.mock_mode = mock_mode or not self.api_key or self.api_key == "tu_api_key_aqui"
        
        # Solo crear cliente si hay API key
        if not self.mock_mode:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️ OpenAI no está instalado. Usando modo mock.")
                self.mock_mode = True
            except Exception as e:
                print(f"⚠️ Error al crear cliente OpenAI: {e}. Usando modo mock.")
                self.mock_mode = True
        else:
            print("ℹ️ Modo MOCK activado - No se harán llamadas reales a la API")
            self.client = None
        
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict:
        """Carga los prompts desde archivo YAML"""
        try:
            prompts_path = Path(__file__).parent.parent.parent / "prompts" / "prompts.yaml"
            if prompts_path.exists():
                with open(prompts_path, 'r') as f:
                    return yaml.safe_load(f)
        except Exception:
            pass
        return {}
    
    def generate(self, 
                 prompt_key: str, 
                 variables: Dict[str, Any],
                 system_prompt: Optional[str] = None) -> str:
        """Genera respuesta usando un prompt predefinido o personalizado"""
        
        # Si estamos en modo mock, devolver respuestas simuladas
        if self.mock_mode:
            return self._generate_mock_response(prompt_key, variables)
        
        # Obtener template del prompt
        template = self.prompts.get(prompt_key, {})
        user_prompt = template.get('user', '')
        system_default = template.get('system', '')
        
        # Formatear con variables
        try:
            formatted_prompt = user_prompt.format(**variables)
        except KeyError:
            formatted_prompt = user_prompt
        
        # Construir mensajes
        messages = []
        if system_prompt or system_default:
            messages.append({
                "role": "system",
                "content": system_prompt or system_default
            })
        
        messages.append({"role": "user", "content": formatted_prompt})
        
        try:
            # Llamada a la API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Error en llamada a API: {e}. Usando mock.")
            return self._generate_mock_response(prompt_key, variables)
    
    def _generate_mock_response(self, prompt_key: str, variables: Dict[str, Any]) -> str:
        """Genera respuestas simuladas para modo mock"""
        
        # Extraer texto si existe
        texto = variables.get('texto', '')
        texto_lower = texto.lower()
        
        if prompt_key == "sentiment" or prompt_key == "sentiment_short":
            # Simular análisis de sentimiento
            if "excelente" in texto_lower or "bueno" in texto_lower or "recomendable" in texto_lower:
                return "positivo"
            elif "malo" in texto_lower or "pésimo" in texto_lower or "terrible" in texto_lower:
                return "negativo"
            else:
                return "neutral"
        
        elif prompt_key == "summarizer":
            # Simular resumen
            max_palabras = variables.get('max_palabras', 100)
            palabras = texto.split()[:max_palabras]
            return " ".join(palabras[:20]) + "..."  # Resumen corto simulado
        
        elif prompt_key == "keywords":
            # Simular extracción de keywords
            n = variables.get('n', 5)
            palabras = texto.split()
            # Tomar algunas palabras comunes
            palabras_comunes = ["tecnología", "innovación", "digital", "transformación", "industria"]
            return ", ".join(palabras_comunes[:n])
        
        elif prompt_key == "combined_analysis":
            return f"""📊 Análisis combinado (MOCK):
            
Basado en el texto proporcionado, se observa que el contenido aborda temas relevantes.
El sentimiento general es positivo con algunas consideraciones importantes.
Se recomienda prestar atención a los puntos clave identificados en el análisis."""
        
        else:
            return f"Respuesta mock para {prompt_key}"