"""
Pruebas unitarias para el agente personalizado
"""
import pytest
import os
from unittest.mock import Mock, patch
from src.core.agent import BaseAgent
from src.core.llm_client import LLMClient
from src.skills.base_skill import BaseSkill
from src.agents.text_analyst_agent import TextAnalystAgent
from src.skills.sentiment_skill import SentimentSkill
from src.skills.summarizer_skill import SummarizerSkill
from src.skills.keyword_skill import KeywordSkill

# ============ TESTS PARA BASEAGENT ============

class TestBaseAgent:
    """Pruebas para la clase BaseAgent"""
    
    def test_agent_initialization(self):
        """Prueba la inicialización básica del agente"""
        agent = BaseAgent(name="TestAgent")
        assert agent.name == "TestAgent"
        assert isinstance(agent.skills, dict)
        assert len(agent.skills) == 0
        assert agent.max_history == 10
    
    def test_agent_with_config(self):
        """Prueba la inicialización con configuración"""
        config = {
            "role": "tester",
            "style": "metódico",
            "context": "Contexto de prueba"
        }
        agent = BaseAgent(name="ConfigAgent", config=config)
        assert agent.role == "tester"
        assert agent.style == "metódico"
        assert agent.context == "Contexto de prueba"
    
    def test_add_skill(self):
        """Prueba agregar una skill al agente"""
        agent = BaseAgent(name="SkillAgent")
        mock_skill = Mock(spec=BaseSkill)
        
        # Agregar skill
        result = agent.add_skill("test_skill", mock_skill)
        assert result is True
        assert "test_skill" in agent.skills
        
        # Intentar agregar skill duplicada
        result = agent.add_skill("test_skill", mock_skill)
        assert result is False
    
    def test_remove_skill(self):
        """Prueba eliminar una skill del agente"""
        agent = BaseAgent(name="SkillAgent")
        mock_skill = Mock(spec=BaseSkill)
        agent.add_skill("test_skill", mock_skill)
        
        # Eliminar skill existente
        result = agent.remove_skill("test_skill")
        assert result is True
        assert "test_skill" not in agent.skills
        
        # Intentar eliminar skill inexistente
        result = agent.remove_skill("nonexistent")
        assert result is False
    
    def test_get_skill(self):
        """Prueba obtener una skill"""
        agent = BaseAgent(name="SkillAgent")
        mock_skill = Mock(spec=BaseSkill)
        mock_skill.description = "Skill de prueba"
        agent.add_skill("test_skill", mock_skill)
        
        # Obtener skill existente
        skill = agent.get_skill("test_skill")
        assert skill == mock_skill
        
        # Obtener skill inexistente
        skill = agent.get_skill("nonexistent")
        assert skill is None
    
    def test_list_skills(self):
        """Prueba listar todas las skills"""
        agent = BaseAgent(name="SkillAgent")
        
        # Sin skills
        skills = agent.list_skills()
        assert skills == {}
        
        # Con skills
        skill1 = Mock(spec=BaseSkill)
        skill1.description = "Skill 1"
        skill2 = Mock(spec=BaseSkill)
        skill2.description = "Skill 2"
        
        agent.add_skill("skill1", skill1)
        agent.add_skill("skill2", skill2)
        
        skills = agent.list_skills()
        assert skills == {"skill1": "Skill 1", "skill2": "Skill 2"}
    
    def test_execute_skill(self):
        """Prueba ejecutar una skill"""
        agent = BaseAgent(name="SkillAgent")
        mock_skill = Mock(spec=BaseSkill)
        mock_skill.execute.return_value = "resultado"
        agent.add_skill("test_skill", mock_skill)
        
        # Ejecutar skill existente
        result = agent.execute_skill("test_skill", param="value")
        assert result == "resultado"
        mock_skill.execute.assert_called_once_with(param="value")
        
        # Ejecutar skill inexistente
        with pytest.raises(KeyError):
            agent.execute_skill("nonexistent")
    
    def test_history_management(self):
        """Prueba la gestión del historial"""
        agent = BaseAgent(name="HistoryAgent", config={"max_history": 2})
        
        # Agregar mensajes
        agent.add_to_history({"role": "user", "content": "Mensaje 1"})
        agent.add_to_history({"role": "assistant", "content": "Mensaje 2"})
        assert len(agent.history) == 2
        
        # Verificar límite de historial
        agent.add_to_history({"role": "user", "content": "Mensaje 3"})
        assert len(agent.history) == 2
        assert agent.history[0]["content"] == "Mensaje 2"
        assert agent.history[1]["content"] == "Mensaje 3"
        
        # Limpiar historial
        agent.clear_history()
        assert len(agent.history) == 0
    
    def test_update_config(self):
        """Prueba actualizar configuración"""
        agent = BaseAgent(name="ConfigAgent")
        agent.update_config({
            "role": "nuevo_rol",
            "style": "nuevo_estilo"
        })
        assert agent.role == "nuevo_rol"
        assert agent.style == "nuevo_estilo"

# ============ TESTS PARA TEXTANALYSTAGENT ============

class TestTextAnalystAgent:
    """Pruebas para el TextAnalystAgent"""
    
    @pytest.fixture
    def agent(self):
        """Fixture para crear un agente de prueba"""
        return TextAnalystAgent(
            name="TestAnalyst",
            config={
                "role": "analista de prueba",
                "style": "práctico",
                "enable_combined_analysis": False  # Desactivar para tests
            }
        )
    
    def test_agent_initialization(self, agent):
        """Prueba la inicialización del agente"""
        assert agent.name == "TestAnalyst"
        assert agent.role == "analista de prueba"
        assert "sentiment" in agent.skills
        assert "summarizer" in agent.skills
        assert "keywords" in agent.skills
    
    def test_analyze_text_with_all_skills(self, agent):
        """Prueba análisis de texto con todas las skills"""
        texto = "Este es un texto de prueba para análisis."
        
        # Mockear las skills para evitar llamadas a API
        with patch.object(agent.skills['sentiment'], 'execute') as mock_sentiment, \
             patch.object(agent.skills['summarizer'], 'execute') as mock_summarizer, \
             patch.object(agent.skills['keywords'], 'execute') as mock_keywords:
            
            mock_sentiment.return_value = {"sentimiento": "positivo"}
            mock_summarizer.return_value = {"resumen": "Resumen de prueba"}
            mock_keywords.return_value = {"palabras_clave": ["prueba", "texto"]}
            
            resultado = agent.analyze_text(texto)
            
            assert "texto" in resultado
            assert "longitud" in resultado
            assert "analisis" in resultado
            assert "sentiment" in resultado["analisis"]
            assert "summarizer" in resultado["analisis"]
            assert "keywords" in resultado["analisis"]
    
    def test_analyze_text_with_specific_skills(self, agent):
        """Prueba análisis con skills específicas"""
        texto = "Texto de prueba"
        
        with patch.object(agent.skills['sentiment'], 'execute') as mock_sentiment:
            mock_sentiment.return_value = {"sentimiento": "neutral"}
            
            resultado = agent.analyze_text(texto, skills=["sentiment"])
            
            assert "sentiment" in resultado["analisis"]
            assert "summarizer" not in resultado["analisis"]
            assert "keywords" not in resultado["analisis"]
    
    def test_analyze_text_empty(self, agent):
        """Prueba análisis con texto vacío"""
        resultado = agent.analyze_text("")
        assert "error" in resultado
        assert resultado["error"] == "El texto no puede estar vacío"
    
    def test_list_skills(self, agent):
        """Prueba listar skills del agente"""
        skills = agent.list_skills()
        assert len(skills) == 3
        assert "sentiment" in skills
        assert "summarizer" in skills
        assert "keywords" in skills
    
    def test_add_new_skill(self, agent):
        """Prueba agregar una nueva skill"""
        new_skill = Mock(spec=BaseSkill)
        new_skill.description = "Nueva skill"
        
        agent.add_skill("new_skill", new_skill)
        assert "new_skill" in agent.skills
        assert agent.skills["new_skill"] == new_skill
    
    def test_update_config(self, agent):
        """Prueba actualizar configuración del agente"""
        new_config = {
            "style": "creativo",
            "summary_length": 50
        }
        agent.update_config(new_config)
        
        assert agent.style == "creativo"
        assert agent.config["summary_length"] == 50
    
    def test_get_config(self, agent):
        """Prueba obtener configuración"""
        config = agent.get_config()
        assert "name" in config
        assert "role" in config
        assert "style" in config
        assert config["name"] == "TestAnalyst"

# ============ TESTS DE INTEGRACIÓN ============

class TestIntegration:
    """Pruebas de integración entre componentes"""
    
    @pytest.fixture
    def agent(self):
        """Fixture para pruebas de integración"""
        return TextAnalystAgent()
    
    def test_skills_integration(self, agent):
        """Prueba que las skills funcionen juntas"""
        # Verificar que todas las skills estén inicializadas
        assert all(skill in agent.skills for skill in ["sentiment", "summarizer", "keywords"])
        
        # Verificar que cada skill tenga el cliente LLM
        for skill in agent.skills.values():
            assert hasattr(skill, 'llm_client')
            assert skill.llm_client is not None
    
    def test_agent_skill_consistency(self, agent):
        """Prueba consistencia entre agente y skills"""
        # Verificar que las skills del agente tengan nombres consistentes
        skill_names = agent.list_skills()
        
        for name in skill_names:
            skill = agent.get_skill(name)
            assert skill is not None
            assert skill.name == name or skill.name.endswith(name) or name in skill.name

# ============ TEST DE PERFORMANCE ============

class TestPerformance:
    """Pruebas de performance"""
    
    def test_agent_creation_performance(self, benchmark):
        """Prueba tiempo de creación del agente"""
        def create_agent():
            return TextAnalystAgent()
        
        result = benchmark(create_agent)
        assert result is not None
    
    def test_skill_lookup_performance(self, benchmark):
        """Prueba eficiencia de búsqueda de skills"""
        agent = TextAnalystAgent()
        
        def lookup_skill():
            return agent.get_skill("sentiment")
        
        result = benchmark(lookup_skill)
        assert result is not None

# ============ UTILIDADES DE PRUEBA ============

class MockLLMClient:
    """Mock del cliente LLM para pruebas"""
    
    def generate(self, prompt_key, variables, system_prompt=None):
        return "Respuesta mock de prueba"

def create_test_agent():
    """Crea un agente de prueba con configuración simple"""
    return TextAnalystAgent(
        name="TestAgent",
        config={
            "role": "tester",
            "style": "simple",
            "enable_combined_analysis": False
        }
    )

# Configuración para ejecutar pruebas
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])