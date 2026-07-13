#!/usr/bin/env python3
"""
Script principal para ejecutar el agente con API real
"""
import sys
import os
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.text_analyst_agent import TextAnalystAgent
from src.config.settings import settings, get_settings

def main():
    """Función principal"""
    print("="*60)
    print("🚀 SISTEMA AGENTICO - ANÁLISIS DE TEXTO")
    print("="*60)
    
    # Verificar si existe API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "tu_api_key_aqui":
        print("\n⚠️  No se encontró API Key de OpenAI")
        print("📝 El sistema funcionará en modo de prueba (sin llamadas reales a la API)")
        print("   Para usar la API real, configura OPENAI_API_KEY en el archivo .env\n")
        usar_api = False
    else:
        print("\n✅ API Key encontrada")
        usar_api = True
    
    # Crear agente
    agent = TextAnalystAgent(
        name="AnalistaPro",
        config={
            "role": "experto en análisis de texto",
            "style": "profesional y detallado",
            "enable_combined_analysis": usar_api,  # Solo si hay API
            "summary_length": 80,
            "keywords_count": 5
        }
    )
    
    print("\n📊 Configuración del agente:")
    config = agent.get_config()
    print(f"  • Nombre: {config['name']}")
    print(f"  • Rol: {config['role']}")
    print(f"  • Estilo: {config['style']}")
    print(f"  • Skills disponibles: {len(agent.skills)}")
    
    # Texto de ejemplo
    texto = """
    La inteligencia artificial está transformando rápidamente la industria tecnológica. 
    Empresas de todo el mundo están implementando soluciones basadas en IA para mejorar 
    sus procesos y servicios. Sin embargo, también surgen desafíos éticos importantes 
    que deben ser abordados con responsabilidad.
    """
    
    print("\n" + "="*60)
    print("📝 Texto a analizar:")
    print("-"*60)
    print(texto.strip())
    print("-"*60)
    print(f"📊 Longitud: {len(texto.split())} palabras")
    
    print("\n⏳ Analizando...")
    
    try:
        # Ejecutar análisis
        resultado = agent.analyze_text(texto)
        
        print("\n" + "="*60)
        print("📊 RESULTADOS DEL ANÁLISIS:")
        print("="*60)
        
        # Mostrar resultados de cada skill
        if "analisis" in resultado:
            for skill_name, skill_result in resultado["analisis"].items():
                print(f"\n🎯 {skill_name.upper()}:")
                if "error" in skill_result:
                    print(f"  ❌ Error: {skill_result['error']}")
                else:
                    for key, value in skill_result.items():
                        if key != "texto_original":
                            print(f"  • {key}: {value}")
        
        # Mostrar análisis combinado si existe
        if "analisis_combinado" in resultado and usar_api:
            print("\n" + "="*60)
            print("💡 ANÁLISIS COMBINADO:")
            print("="*60)
            print(resultado["analisis_combinado"])
        
        print("\n" + "="*60)
        print("✅ Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        print("\n💡 Sugerencia: Si no tienes API key, ejecuta 'python test_system.py' para probar la estructura")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())