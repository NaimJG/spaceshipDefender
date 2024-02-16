import pygame
import sys
import random
import math

pygame.init()

ANCHO = 800
ALTO = 600
white = (255, 255, 255)
grey = (155, 155, 155)

screen = pygame.display.set_mode((ANCHO, ALTO))


# Estrellas
stars = []

# Función para generar estrellas
def spawn_star():
    angle = random.uniform(0, 2 * math.pi)  # Ángulo aleatorio
    speed = random.uniform(3, 4)  # Velocidad aleatoria
    x = ANCHO // 2 + speed * math.cos(angle)
    y = ALTO // 2 + speed * math.sin(angle)
    stars.append([x, y, angle, speed])

# Función para calcular la distancia entre dos puntos
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Bucle principal
clock = pygame.time.Clock()
spawn_timer = 0
star_spawn_timer = 0

while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()

    # Generar pixeles blancos aleatorios
    star_spawn_timer += 1
    if star_spawn_timer == 2:  # Generar cada 10 frames
        spawn_star()
        star_spawn_timer = 0

    # Actualizar la posición de los pixeles blancos
    for star in stars:
        angle = star[2]
        speed = star[3]
        star[0] += speed * math.cos(angle)
        star[1] += speed * math.sin(angle)

    # Eliminar estrellas que salen de la pantalla
    stars = [star for star in stars if 0 <= star[0] < ANCHO and 0 <= star[1] < ALTO]


    screen.fill((0,0,0))

    pygame.draw.line(screen, grey, [0, 80], [193, 167], 8)
    pygame.draw.line(screen, grey, [605, 433], [ANCHO, 550], 8)

    pygame.draw.line(screen, grey, [ANCHO, 80], [605, 167], 8)
    pygame.draw.line(screen, grey, [0, 550], [195, 433], 8)

    pygame.draw.circle(screen, grey, (ANCHO//2, ALTO//2), 250, 8)

    # Dibujar líneas cortas para representar estrellas
    for star in stars:
        end_point = (int(star[0] + 8 * math.cos(star[2])), int(star[1] + 8 * math.sin(star[2])))
        pygame.draw.line(screen, white, (int(star[0]), int(star[1])), end_point, 2)


    pygame.display.flip()
    clock.tick(60)
