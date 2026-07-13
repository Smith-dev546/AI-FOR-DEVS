# 🧠 Sistema Agentico Refactorizado - Analista de Texto

[![Estado](https://img.shields.io/badge/Estado-Funcionando-brightgreen)]()
[![Pruebas](https://img.shields.io/badge/Pruebas-8%2F8-success)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()

## 📌 Descripción

Sistema agentico modular para análisis de texto con skills personalizables. Este proyecto demuestra la refactorización de un sistema monolítico a una arquitectura basada en agentes con habilidades (skills) desacopladas.

### 🎯 Características Principales

- ✅ **Arquitectura modular**: Separación clara de responsabilidades
- ✅ **Skills reutilizables**: Sentimiento, resumen y palabras clave
- ✅ **Agentes personalizables**: Configuración dinámica del comportamiento
- ✅ **Modo MOCK**: Funciona sin API key para pruebas
- ✅ **Pruebas unitarias**: 8/8 pruebas pasando

---

## 🏗️ Arquitectura
```bash
📁 proyecto_refactorizado/
├── 📁 src/
│   ├── 📁 core/                    # Componentes centrales
│   │   ├── llm_client.py           # Cliente LLM configurable
│   │   └── agent.py                # Clase base para agentes
│   ├── 📁 skills/                  # Habilidades del sistema
│   │   ├── base_skill.py           # Interfaz de skill
│   │   ├── sentiment_skill.py      # Skill de sentimiento
│   │   ├── summarizer_skill.py     # Skill de resumen
│   │   └── keyword_skill.py        # Skill de palabras clave
│   ├── 📁 agents/                  # Agentes específicos
│   │   └── text_analyst_agent.py   # Agente analista de texto
│   └── 📁 config/                  # Configuración centralizada
│       └── settings.py             # Configuración del sistema
├── 📁 prompts/                     # Prompts externalizados
│   └── prompts.yaml                # Archivo de prompts
├── 📁 tests/                       # Pruebas unitarias
│   └── test_agent.py               # Pruebas del agente
├── 📄 main.py                      # Punto de entrada principal
├── 📄 run_agent.py                 # Script de ejecución rápida
├── 📄 test_system.py               # Suite de pruebas
├── 📄 requirements.txt             # Dependencias
├── 📄 .env.example                 # Variables de entorno
└── 📄 README.md                    # Este archivo
```

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar o descargar el proyecto

```bash
cd proyecto_refactorizado
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar variables de entorno (OPCIONAL)
Si tienes API key de OpenAI, crea el archivo .env:

```bash
# Copiar el ejemplo
copy .env.example .env

# Editar con tu API key
notepad .env

```

### 🧪 Cómo Probar el Sistema
✅ Prueba 1: Verificar instalación (Recomendado)
Ejecuta la suite de pruebas para verificar que todo funciona:

```bash
python test_system.py

```
### 🚀 Prueba 2: Ejecutar el agente (Modo MOCK)
Ejecuta el agente con un texto de ejemplo:

```bash
python run_agent.py
```

### 🔧 Prueba 3: Ejecutar el agente (Con API Real)
Si tienes API key de OpenAI:

Configura tu API key en .env

Ejecuta:

```bash
python run_agent.py
```