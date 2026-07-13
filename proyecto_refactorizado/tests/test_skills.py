
### tests/test_skills.py
import pytest
from src.skills.sentiment_skill import SentimentSkill
from src.skills.summarizer_skill import SummarizerSkill
from src.skills.keyword_skill import KeywordSkill

def test_sentiment_skill_basic():
    skill = SentimentSkill()
    texto = "Este producto es excelente"
    resultado = skill.execute(texto=texto)
    assert "sentimiento" in resultado
    assert resultado["sentimiento"] in ["positivo", "negativo", "neutral"]

def test_summarizer_skill():
    skill = SummarizerSkill()
    texto = "Texto largo de prueba..." * 10
    resultado = skill.execute(texto=texto, max_palabras=20)
    assert "resumen" in resultado

def test_keyword_skill():
    skill = KeywordSkill()
    texto = "Python es un lenguaje de programación excelente"
    resultado = skill.execute(texto=texto, n=3)
    assert "palabras_clave" in resultado
    assert len(resultado["palabras_clave"]) <= 3