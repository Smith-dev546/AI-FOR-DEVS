import pygame
import random
import math

# 1. Inicializar Pygame y configurar la pantalla
pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Atrapa la Fruta - Edición Especial")

# 2. Paleta de colores extendida
COLOR_FONDO = (0, 0, 0)        # Negro
COLOR_TEXTO = (255, 255, 255)  # Blanco
COLOR_GAMEOVER = (255, 50, 50)  # Rojo brillante para el Game Over

# Colores de la cesta basados en la racha
COLOR_CESTA_BAJA = (0, 255, 0)      # Verde
COLOR_CESTA_MEDIA = (255, 220, 0)    # Amarillo
COLOR_CESTA_ALTA = (255, 100, 0)     # Rojo/Naranja

# Lista de colores posibles para la fruta
COLORES_FRUTA = [
    (255, 0, 0),    # Rojo
    (0, 100, 255),  # Azul
    (255, 220, 0),  # Amarillo
    (0, 255, 150)   # Verde fruta
]

# 3. Configuración de la Cesta
ancho_cesta = 100
alto_cesta = 20
cesta_x = (ANCHO_VENTANA - ancho_cesta) // 2
cesta_y = ALTO_VENTANA - alto_cesta - 10
velocidad_cesta = 10
color_actual_cesta = COLOR_CESTA_BAJA

# 4. Configuración de la Fruta
radio_fruta = 15
fruta_x = random.randint(radio_fruta, ANCHO_VENTANA - radio_fruta)
fruta_y = 0
velocidad_fruta_y = 5
color_actual_fruta = random.choice(COLORES_FRUTA)

# Variables para el efecto Zigzag
amplitud_zigzag = 3   
frecuencia_zigzag = 0.1 

# 5. Marcadores, Racha y Fuentes
vidas = 3
puntos = 0
racha = 0  # NUEVO: Contador de racha consecutiva
fuente_marcador = pygame.font.SysFont(None, 36)
fuente_gameover = pygame.font.SysFont(None, 72)
fuente_reinicio = pygame.font.SysFont(None, 28)

# NUEVO: Sistema de partículas (Destello)
# Guardará diccionarios con: [x, y, radio_actual, color, opacidad]
particulas = []

# Variables de control de estado
reloj = pygame.time.Clock()
jugando = True
estado_game_over = False  

# Bucle principal del juego
while jugando:
    reloj.tick(60)

    # 6. Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        
        if evento.type == pygame.KEYDOWN and estado_game_over:
            if evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN:
                # Reiniciar todas las variables del juego
                vidas = 3
                puntos = 0
                racha = 0
                velocidad_fruta_y = 5
                fruta_y = 0
                fruta_x = random.randint(radio_fruta, ANCHO_VENTANA - radio_fruta)
                color_actual_fruta = random.choice(COLORES_FRUTA)
                cesta_x = (ANCHO_VENTANA - ancho_cesta) // 2
                color_actual_cesta = COLOR_CESTA_BAJA
                particulas.clear()
                estado_game_over = False

    # 7. Lógica del juego activo
    if not estado_game_over:
        # Movimiento de la cesta con el teclado
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and cesta_x > 0:
            cesta_x -= velocidad_cesta
        if teclas[pygame.K_RIGHT] and cesta_x < ANCHO_VENTANA - ancho_cesta:
            cesta_x += velocidad_cesta

        # Actualizar color de la cesta según la racha
        if racha < 5:
            color_actual_cesta = COLOR_CESTA_BAJA
        elif racha < 10:
            color_actual_cesta = COLOR_CESTA_MEDIA
        else:
            color_actual_cesta = COLOR_CESTA_ALTA

        # Movimiento vertical y horizontal en Zigzag de la fruta
        fruta_y += velocidad_fruta_y
        fruta_x += math.sin(fruta_y * frecuencia_zigzag) * amplitud_zigzag
        
        if fruta_x < radio_fruta:
            fruta_x = radio_fruta
        elif fruta_x > ANCHO_VENTANA - radio_fruta:
            fruta_x = ANCHO_VENTANA - radio_fruta

        # Comprobar si la fruta toca el suelo (pierde vida y rompe racha)
        if fruta_y > ALTO_VENTANA:
            vidas -= 1
            racha = 0  # NUEVO: La racha se pierde si la fruta cae
            fruta_y = 0
            fruta_x = random.randint(radio_fruta, ANCHO_VENTANA - radio_fruta)
            color_actual_fruta = random.choice(COLORES_FRUTA)
            
            if vidas <= 0:
                estado_game_over = True 

        # Detección de colisiones (Atrapar la fruta)
        if (cesta_x < fruta_x < cesta_x + ancho_cesta) and \
           (cesta_y < fruta_y + radio_fruta < cesta_y + alto_cesta):
            puntos += 1
            racha += 1  # NUEVO: Incrementa racha consecutiva
            velocidad_fruta_y += 0.2 
            
            # NUEVO: Crear partículas de destello usando el color de la fruta atrapada
            for _ in range(12):  
                particulas.append({
                    "x": fruta_x,
                    "y": fruta_y,
                    "vx": random.uniform(-4, 4), # Velocidad horizontal aleatoria
                    "vy": random.uniform(-4, 2), # Velocidad vertical aleatoria
                    "radio": random.randint(4, 8),
                    "color": color_actual_fruta,
                    "vida": 255 # Opacidad/Tiempo de vida inicial
                })

            # Reiniciar fruta
            fruta_y = 0
            fruta_x = random.randint(radio_fruta, ANCHO_VENTANA - radio_fruta)
            color_actual_fruta = random.choice(COLORES_FRUTA)

    # NUEVO: Actualizar la lógica de las partículas (incluso en Game Over si quedaron flotando)
    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["radio"] += 0.2  # Se expande un poco
        p["vida"] -= 8     # Se desvanece gradualmente
        if p["vida"] <= 0:
            particulas.remove(p)

    # 8. Renderizado y Dibujo en pantalla
    ventana.fill(COLOR_FONDO)  
    
    # NUEVO: Dibujar partículas con transparencia usando una superficie auxiliar
    for p in particulas:
        surf_particula = pygame.Surface((int(p["radio"] * 2), int(p["radio"] * 2)), pygame.SRCALPHA)
        color_con_alfa = (p["color"][0], p["color"][1], p["color"][2], max(0, p["vida"]))
        pygame.draw.circle(surf_particula, color_con_alfa, (int(p["radio"]), int(p["radio"])), int(p["radio"]))
        ventana.blit(surf_particula, (int(p["x"] - p["radio"]), int(p["y"] - p["radio"])))

    if not estado_game_over:
        # Dibujar elementos del juego activo
        pygame.draw.rect(ventana, color_actual_cesta, (cesta_x, cesta_y, ancho_cesta, alto_cesta))
        pygame.draw.circle(ventana, color_actual_fruta, (int(fruta_x), int(fruta_y)), radio_fruta)

        # Dibujar puntuación, vidas y RACHA
        texto_puntos = fuente_marcador.render(f"Puntos: {puntos}", True, COLOR_TEXTO)
        texto_vidas = fuente_marcador.render(f"Vidas: {vidas}", True, COLOR_TEXTO)
        texto_racha = fuente_marcador.render(f"Racha: {racha}", True, color_actual_cesta) # Toma el color de la cesta
        
        ventana.blit(texto_puntos, (10, 10))
        ventana.blit(texto_racha, (10, 45))
        ventana.blit(texto_vidas, (ANCHO_VENTANA - 120, 10))
    else:
        # Dibujar textos de GAME OVER
        texto_go = fuente_gameover.render("¡GAME OVER!", True, COLOR_GAMEOVER)
        texto_reiniciar = fuente_reinicio.render("Presiona ESPACIO o ENTER para volver a jugar", True, COLOR_TEXTO)
        texto_score = fuente_marcador.render(f"Puntuación final: {puntos}", True, COLOR_TEXTO)
        
        ventana.blit(texto_go, (ANCHO_VENTANA // 2 - texto_go.get_width() // 2, ALTO_VENTANA // 2 - 80))
        ventana.blit(texto_score, (ANCHO_VENTANA // 2 - texto_score.get_width() // 2, ALTO_VENTANA // 2))
        ventana.blit(texto_reiniciar, (ANCHO_VENTANA // 2 - texto_reiniciar.get_width() // 2, ALTO_VENTANA // 2 + 60))

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
