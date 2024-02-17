import pygame
import sys
import random
import math

pygame.init()

ANCHO = 800
ALTO = 600
white = (255, 255, 255)
grey = (155, 155, 155)
dark_grey = (100, 100, 100)
darker_grey = (85, 85, 85)

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.mouse.set_visible(0)

# Estrellas
stars = []

class Crossair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen original
        self.image_original = pygame.image.load('mira.png')
        # Escalar la imagen a 30x30
        self.escalar(70, 70)

    def escalar(self, width, height):
        # Escalar la imagen
        self.image = pygame.transform.scale(self.image_original, (width, height))
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()

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

mira = Crossair()

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

    # Dibujar líneas cortas para representar estrellas
    for star in stars:
        end_point = (int(star[0] + 8 * math.cos(star[2])), int(star[1] + 8 * math.sin(star[2])))
        pygame.draw.line(screen, white, (int(star[0]), int(star[1])), end_point, 2)


    points = [(0, 78), (194, 165), (189, 171), (0, 100)]
    pygame.draw.polygon(screen, grey, points)

    points = [(ANCHO, 78), (606, 165), (611, 171), (ANCHO, 100)]
    pygame.draw.polygon(screen, grey, points)

    pygame.draw.circle(screen, grey, (ANCHO//2, ALTO//2), 250, 8)

    # Rellenar la sección entre las dos líneas inferiores y el círculo
    points = [(-100, ALTO), (190, 433), (ANCHO//2, ALTO//2 + 120), (610, 433), (ANCHO + 100, ALTO)]
    pygame.draw.polygon(screen, dark_grey, points)

    # Rellenar la sección entre las dos líneas inferiores y el círculo
    points = [(70, ALTO), (200, 495), (ANCHO//2, ALTO//2 + 180), (595, 495), (ANCHO - 70, ALTO)]
    pygame.draw.polygon(screen, darker_grey, points)

    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    # Dibujar mira en pantalla
    screen.blit(mira.image, (mouse_x - mira.rect.width // 2, mouse_y - mira.rect.height // 2))

    pygame.display.flip()
    clock.tick(60)
