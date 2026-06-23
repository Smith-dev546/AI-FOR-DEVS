# 🎮 Atrapa la Fruta - Vibecoding con IA

**Autor:** José Smith Méndez Hernández
**Fecha:** 22/06/26
**Herramientas:** Python 3.14.6, Pygame, Gemini (IA)

---

## 📋 Descripción del Proyecto

Juego interactivo "Atrapa la Fruta" desarrollado con técnicas de **vibecoding**, utilizando IA como asistente de programación. El jugador controla una cesta para atrapar frutas que caen, acumulando puntos y rachas mientras gestiona vidas.

### Características principales:
- 🎯 Movimiento de cesta con flechas ← →
- 🍎 Frutas con colores aleatorios
- 📊 Sistema de puntuación y vidas
- 🔥 Sistema de racha con cambio de color de cesta
- ✨ Efecto de partículas al atrapar fruta
- 🌀 Movimiento zigzag de las frutas
- 🎮 Pantalla de Game Over con reinicio

---

## 🤖 Prompts Utilizados

### Prompt #1 - Creación inicial

Quiero crear un juego simple en Python usando Pygame. El juego debe ser "Atrapa la fruta" donde: 
- Una fruta (círculo rojo) cae desde arriba 
- El jugador controla una cesta (rectángulo verde) con las flechas izquierda/derecha 
- Cada fruta atrapada suma 1 punto - Si la fruta toca el fondo, se pierde una vida (empiezas con 3 vidas) 
- Debe mostrar la puntuación y vidas en la pantalla 
- El juego termina cuando las vidas llegan a 0 Genérame el código completo y explicame cada parte.


**¿Qué pedí?**
Solicité un juego base completo de "Atrapa la fruta" con mecánicas esenciales: movimiento de cesta, caída de fruta, puntuación, vidas y condición de Game Over.

**¿Por qué este prompt?**
Quería una base funcional desde el inicio para poder iterar sobre ella. Al pedir el código completo con explicaciones, podía entender cada parte y luego mejorarla.

---

### Prompt #2 - Mejoras visuales y funcionales

Tengo un juego de "Atrapa la fruta" que ya funciona. Quiero hacer estas mejoras:

1. Cambiar el color de la fruta aleatoriamente entre rojo, azul, amarillo y verde
2. Mostrar un mensaje de "¡GAME OVER!" en el centro de la pantalla cuando se pierde, en lugar de solo en la consola
3. Agregar un botón o tecla (Espacio o Enter) para reiniciar el juego después del Game Over
4. Hacer que la fruta no solo caiga hacia abajo, sino que también se mueva ligeramente de izquierda a derecha mientras cae (como zigzag)

Modifica el código manteniendo todo lo que ya funciona.


**¿Qué pedí?**
Solicité cambios específicos: colores aleatorios para frutas, mensaje Game Over en pantalla, reinicio con teclas y movimiento zigzag.

**¿Por qué este prompt?**
Las mejoras visuales (colores) hacen el juego más atractivo. El Game Over en pantalla y el reinicio mejoran la experiencia de usuario. El zigzag añade desafío sin complicar demasiado el código.

---

### Prompt #3 - Efectos y mecánicas avanzadas

El juego "Atrapa la fruta" mejorado funciona perfectamente. Ahora quiero añadir estos detalles finales:

1. Efecto de partículas o destello cuando atrapas una fruta (puede ser simple, como un círculo que se expande y desaparece)
2. Un contador de "Racha" que muestre cuántas frutas has atrapado consecutivamente
3. La racha se reinicia a 0 si se te cae una fruta
4. Cambiar el color de la cesta según la racha:
   - Racha 0-4: Verde
   - Racha 5-9: Amarillo
   - Racha 10+: Rojo/Naranja

Mantén todo el código existente y añade estas nuevas funciones.


**¿Qué pedí?**
Solicité sistema de partículas, contador de racha, reinicio de racha al fallar y cambio de color de cesta según racha.

**¿Por qué este prompt?**
Quería añadir profundidad al juego. Las partículas dan feedback visual satisfactorio. La racha añade un elemento estratégico y el cambio de color es un indicador visual claro del rendimiento.

---

## 🔄 Iteraciones y Mejoras

### Iteración 1 (Prompt #1 → #2)
| Mejora | Descripción | Impacto |
|--------|-------------|---------|
| Colores aleatorios | Frutas con colores variables | Visualmente más atractivo |
| Game Over en pantalla | Mensaje grande en centro | Mejor UX que solo consola |
| Reinicio con tecla | Espacio o Enter para reiniciar | Rejugabilidad inmediata |
| Movimiento zigzag | Fruta se mueve lateralmente | Mayor desafío |

### Iteración 2 (Prompt #2 → #3)
| Mejora | Descripción | Impacto |
|--------|-------------|---------|
| Sistema de partículas | Destello al atrapar fruta | Feedback visual satisfactorio |
| Contador de racha | Muestra capturas consecutivas | Añade motivación |
| Reinicio de racha | Se pierde al fallar | Añade presión y estrategia |
| Color dinámico de cesta | Verde→Amarillo→Rojo según racha | Indicador visual de rendimiento |

---

## 🧪 Validación del Código

### Pruebas realizadas
1. ✅ Ejecución inicial sin errores
2. ✅ Movimiento de cesta con flechas izquierda/derecha
3. ✅ Captura de frutas sumando puntos correctamente
4. ✅ Pérdida de vidas cuando fruta cae
5. ✅ Game Over al llegar a 0 vidas
6. ✅ Reinicio del juego con ESPACIO o ENTER
7. ✅ Colores aleatorios en cada fruta
8. ✅ Movimiento zigzag de frutas
9. ✅ Sistema de partículas al atrapar
10. ✅ Contador de racha y cambio de color de cesta

---

## 💭 Reflexión Final

### ¿Qué aprendí usando IA para programar?

Aprendí que la IA es una herramienta poderosa para generar código base y realizar iteraciones rápidas. El proceso de vibecoding me enseñó a ser más específico en mis peticiones y a entender la estructura del código generado. Descubrí que la clave no es solo pedir código, sino entenderlo y saber cómo mejorarlo.

### Ventajas del vibecoding
- ⚡ **Velocidad:** Genera código funcional en segundos
- 🔄 **Iteración rápida:** Fácil probar diferentes enfoques
- 📚 **Aprendizaje:** Ver código bien estructurado ayuda a aprender
- 🧠 **Creatividad:** Permite enfocarse en ideas en lugar de sintaxis
- 🛠️ **Prototipado:** Excelente para crear MVPs rápidamente

### Límites del vibecoding
- 🐛 **Errores sutiles:** Puede generar bugs difíciles de detectar
- 🎯 **Precisión:** Requiere prompts muy específicos para buenos resultados
- 🧩 **Contexto limitado:** La IA no entiende el proyecto completo
- 🔧 **Dependencia:** Riesgo de no entender el código generado
- 💡 **Originalidad:** Puede producir soluciones genéricas

### Partes del código que comprendo

- La inicialización de Pygame y la ventana
- El bucle principal del juego
- El manejo de eventos (teclado y cierre)
- El movimiento de la cesta con teclas
- La lógica de colisión entre cesta y fruta
- El sistema de puntuación y vidas

### Partes del código que necesito reforzar

- El sistema de partículas (uso de superficies con transparencia)
- La función math.sin para el movimiento zigzag
- El manejo de la opacidad en pygame
- La estructura de datos para las partículas (listas de diccionarios)

---

## 🛠️ Instalación y Ejecución

### Requisitos
- Python 3.6 o superior
- Pygame

### Instalación
```bash
# Instalar Pygame
pip install pygame

# O si usas pip3
pip3 install pygame