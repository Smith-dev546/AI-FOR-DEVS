#!/usr/bin/env python3
"""
Script de prueba del sistema sin necesidad de API key
"""
import sys
import os
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.llm_client import LLMClient
from src.core.agent import BaseAgent
from src.skills.base_skill import BaseSkill
from src.skills.sentiment_skill import SentimentSkill
from src.skills.summarizer_skill import SummarizerSkill
from src.skills.keyword_skill import KeywordSkill
from src.agents.text_analyst_agent import TextAnalystAgent
from src.config.settings import settings, get_settings

def test_imports():
    """Prueba 1: Verificar imports"""
    print("✅ Test 1: Verificando imports...")
    assert LLMClient is not None
    assert BaseAgent is not None
    assert BaseSkill is not None
    assert SentimentSkill is not None
    assert SummarizerSkill is not None
    assert KeywordSkill is not None
    assert TextAnalystAgent is not None
    print("   ✅ Todos los imports funcionan correctamente")
    return True

def test_settings():
    """Prueba 2: Verificar configuración"""
    print("\n✅ Test 2: Verificando configuración...")
    config = get_settings()
    
    # Verificar atributos
    assert hasattr(config, 'llm')
    assert hasattr(config, 'agent')
    assert hasattr(config, 'skills')
    
    print(f"   📊 Configuración LLM: {config.llm.model}")
    print(f"   📊 Configuración Agente: {config.agent.role}")
    print(f"   📊 Configuración Skills: {config.skills.enabled_skills}")
    print("   ✅ Configuración cargada correctamente")
    return True

def test_base_agent():
    """Prueba 3: Verificar BaseAgent"""
    print("\n✅ Test 3: Probando BaseAgent...")
    
    # Crear una implementación concreta para prueba
    class ConcreteAgent(BaseAgent):
        def process(self, input_data, **kwargs):
            return f"Procesado: {input_data}"
    
    # Crear agente concreto
    agent = ConcreteAgent(name="TestAgent", config={"role": "tester"})
    
    # Verificar atributos
    assert agent.name == "TestAgent"
    assert agent.role == "tester"
    assert len(agent.skills) == 0
    
    # Agregar una skill mock
    class MockSkill(BaseSkill):
        def execute(self, **kwargs):
            return "mock result"
    
    mock_skill = MockSkill()
    agent.add_skill("mock", mock_skill)
    assert len(agent.skills) == 1
    
    # Ejecutar skill
    result = agent.execute_skill("mock")
    assert result == "mock result"
    
    # Probar método process
    result = agent.process("Hola mundo")
    assert result == "Procesado: Hola mundo"
    
    print(f"   ✅ Agente '{agent.name}' creado y probado correctamente")
    return True

def test_skills_creation():
    """Prueba 4: Verificar creación de skills"""
    print("\n✅ Test 4: Probando creación de skills...")
    
    # Crear skills
    sentiment = SentimentSkill()
    summarizer = SummarizerSkill()
    keywords = KeywordSkill()
    
    # Verificar atributos
    assert hasattr(sentiment, 'execute')
    assert hasattr(summarizer, 'execute')
    assert hasattr(keywords, 'execute')
    
    # Verificar metadatos
    metadata = sentiment.get_metadata()
    assert 'name' in metadata
    assert 'description' in metadata
    
    print(f"   📊 SentimentSkill: {sentiment.description}")
    print(f"   📊 SummarizerSkill: {summarizer.description}")
    print(f"   📊 KeywordSkill: {keywords.description}")
    print("   ✅ Skills creadas correctamente")
    return True

def test_text_analyst_agent():
    """Prueba 5: Verificar TextAnalystAgent"""
    print("\n✅ Test 5: Probando TextAnalystAgent...")
    
    # Crear agente con configuración
    agent = TextAnalystAgent(
        name="TestAnalyst",
        config={
            "role": "analista de prueba",
            "style": "práctico",
            "enable_combined_analysis": False  # Desactivar para pruebas
        }
    )
    
    # Verificar skills
    skills = agent.list_skills()
    assert len(skills) == 3
    assert "sentiment" in skills
    assert "summarizer" in skills
    assert "keywords" in skills
    
    # Verificar configuración
    config = agent.get_config()
    assert config["name"] == "TestAnalyst"
    assert config["role"] == "analista de prueba"
    
    print(f"   ✅ Agente '{agent.name}' creado con {len(skills)} skills")
    print(f"   📊 Skills disponibles: {', '.join(skills.keys())}")
    return True

def test_agent_analyze_without_api():
    """Prueba 6: Probar análisis sin API (simulado)"""
    print("\n✅ Test 6: Probando estructura de análisis...")
    
    agent = TextAnalystAgent(
        name="TestAnalyst",
        config={"enable_combined_analysis": False}
    )
    
    # Probar análisis
    texto = "Este es un texto de prueba para el análisis"
    resultado = agent.analyze_text(texto)
    
    # Verificar estructura
    assert "texto" in resultado
    assert "longitud" in resultado
    assert "analisis" in resultado
    assert resultado["texto"] == texto
    
    print(f"   📝 Texto: '{texto[:30]}...'")
    print(f"   📊 Longitud: {resultado['longitud']} palabras")
    print(f"   📊 Skills ejecutadas: {len(resultado['analisis'])}")
    print("   ✅ Estructura de análisis correcta")
    return True

def test_settings_update():
    """Prueba 7: Verificar actualización de configuración"""
    print("\n✅ Test 7: Probando actualización de configuración...")
    
    config = get_settings()
    
    # Guardar valores originales
    original_model = config.llm.model
    
    # Actualizar
    config.update_llm_config(model="test-model")
    assert config.llm.model == "test-model"
    
    # Restaurar
    config.update_llm_config(model=original_model)
    assert config.llm.model == original_model
    
    print("   ✅ Configuración actualizada correctamente")
    return True

def test_agent_customization():
    """Prueba 8: Verificar personalización del agente"""
    print("\n✅ Test 8: Probando personalización del agente...")
    
    # Agente con configuración personalizada
    agent = TextAnalystAgent(
        name="Analista Personalizado",
        config={
            "role": "experto en marketing",
            "style": "persuasivo y creativo",
            "custom_system_prompt": "Eres un experto en marketing digital",
            "summary_length": 50,
            "keywords_count": 3
        }
    )
    
    # Verificar personalización
    config = agent.get_config()
    assert config["role"] == "experto en marketing"
    assert config["style"] == "persuasivo y creativo"
    assert config["summary_length"] == 50
    assert config["keywords_count"] == 3
    
    print(f"   ✅ Agente personalizado: '{agent.name}'")
    print(f"   📊 Rol: {agent.role}")
    print(f"   📊 Estilo: {agent.style}")
    return True

def main():
    """Ejecutar todas las pruebas"""
    print("="*60)
    print("🧪 EJECUTANDO PRUEBAS DEL SISTEMA AGENTICO")
    print("="*60)
    
    tests = [
        test_imports,
        test_settings,
        test_base_agent,
        test_skills_creation,
        test_text_analyst_agent,
        test_agent_analyze_without_api,
        test_settings_update,
        test_agent_customization
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ Pasadas: {passed}")
    print(f"   ❌ Fallidas: {failed}")
    print(f"   📈 Total: {len(tests)}")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ El sistema está correctamente estructurado")
        return 0
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisa los errores.")
        return 1

if __name__ == "__main__":
    sys.exit(main())