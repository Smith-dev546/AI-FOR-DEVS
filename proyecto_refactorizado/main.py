import os
import yaml
from dotenv import load_dotenv
from src.core.llm_client import LLMClient
from src.agents.text_analyst_agent import TextAnalystAgent

# Cargar variables de entorno
load_dotenv()

def main():
    # Configuración inicial
    llm_config = {
        "model": os.getenv("MODEL", "gpt-3.5-turbo"),
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("MAX_TOKENS", "500"))
    }
    
    # Crear cliente LLM
    llm_client = LLMClient(**llm_config)
    
    # Configuración del agente personalizado
    agent_config = {
        "role": "experto en análisis de textos",
        "style": "analítico y detallado",
        "context": "Trabajas en una empresa de análisis de datos",
        "summary_length": 80,
        "keywords_count": 7,
        "enable_combined_analysis": True,
        "temperature": 0.8,
        "custom_system_prompt": """
        Eres un analista de textos experto con 10 años de experiencia.
        Te especializas en extraer insights valiosos de cualquier texto.
        Tu estilo es profesional pero accesible.
        Siempre proporcionas contexto y razones para tus análisis.
        """
    }
    
    # Crear el agente personalizado
    agent = TextAnalystAgent(
        name="Analista Premium",
        llm_client=llm_client,
        config=agent_config
    )
    
    # Mostrar skills disponibles
    print("🧠 Skills disponibles:")
    for name, desc in agent.list_skills().items():
        print(f"  - {name}: {desc}")
    
    print("\n" + "="*60)
    
    # Ejemplo de análisis
    texto = """
    El nuevo producto de la empresa ha superado todas las expectativas. 
    Los usuarios reportan una experiencia excepcional y la interfaz es 
    increíblemente intuitiva. Sin embargo, el precio podría ser un 
    obstáculo para algunos segmentos del mercado. En general, la recepción 
    ha sido muy positiva y las ventas están creciendo rápidamente.
    """
    
    print(f"📝 Texto a analizar:\n{texto}\n")
    print("="*60)
    
    # Ejecutar análisis con skills específicas
    resultados = agent.analyze_text(
        texto=texto,
        skills=["sentiment", "summarizer", "keywords"]
    )
    
    # Mostrar resultados
    print("\n📊 RESULTADOS DEL ANÁLISIS:")
    print("-"*40)
    
    for skill, resultado in resultados["analisis"].items():
        print(f"\n🎯 {skill.upper()}:")
        if "error" in resultado:
            print(f"  ❌ Error: {resultado['error']}")
        else:
            for key, value in resultado.items():
                if key != "texto_original":
                    print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("\n🤖 ANÁLISIS COMBINADO:")
    print(resultados["analisis_combinado"])
    
    print("\n" + "="*60)
    print("\n⚙️ Configuración del agente:")
    for key, value in agent.get_config().items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()