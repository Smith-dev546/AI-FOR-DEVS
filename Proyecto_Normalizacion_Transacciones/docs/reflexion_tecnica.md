# 📝 Reflexión Técnica - Sistema de Normalización de Transacciones Multifuente

---

## 1. Introducción

Este documento reflexiona sobre el proceso de desarrollo del Sistema de Normalización de Transacciones Multifuente, destacando las decisiones técnicas clave, el uso estratégico de la Inteligencia Artificial como herramienta de apoyo, y las lecciones aprendidas durante el desarrollo del proyecto.

El objetivo del sistema es normalizar transacciones provenientes de múltiples fuentes con diferentes formatos, validarlas y permitir su exploración a través de una interfaz interactiva.

---

## 2. Decisiones de Diseño Fundamentales

### 2.1 Modelo de Datos Normalizado (Decisión Humana)

El esquema final de datos fue definido completamente por criterio humano, considerando las necesidades del negocio y la compatibilidad entre fuentes:

```python
{
    "id": "string",           # Identificador único de la transacción
    "amount": 99.99,          # Monto en formato numérico (float)
    "currency": "USD",        # Moneda en código ISO 4217 (3 letras)
    "timestamp": "ISO-8601",  # Fecha en formato estandarizado internacional
    "status": "SUCCESS",      # Estado normalizado: SUCCESS | FAILED | PENDING
    "source": "string",       # Fuente original de la transacción
    "original_data": {}       # Datos originales para trazabilidad y auditoría
}