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
        # Escalar la imagen a 70x70
        self.escalar(70, 70)

    def escalar(self, width, height):
        # Escalar la imagen
        self.image = pygame.transform.scale(self.image_original, (width, height))
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.size = 0  # Tamaño inicial
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.growing = True  # Variable para controlar el crecimiento
        self.rotation_speed = random.uniform(-3, 3)  # Velocidad de rotación aleatoria

    def crecer(self):
        if self.growing:
            # Aumentar el tamaño del asteroide
            self.size += 0.5

            # Crear una nueva imagen con fondo transparente
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

            # Copiar y escalar la imagen original al nuevo fondo transparente
            scaled_image = pygame.transform.scale(self.image_original, (self.size, self.size))
            self.image.blit(scaled_image, (0, 0))

            # Rotar la nueva imagen con fondo transparente
            self.image = pygame.transform.rotate(self.image, self.rotation_speed)

            # Actualizar el rectángulo de la imagen
            self.rect = self.image.get_rect(center=self.rect.center)

            # Incrementar el ángulo de rotación
            self.rotation_speed += 0.3  # Puedes ajustar la velocidad de rotación aquí

            # Cuando alcanza un tamaño máximo, dejar de crecer
            if self.size > 220:
                self.growing = False

    def update(self):
        self.crecer()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)  # Superficie transparente
        self.rect = self.image.get_rect(topleft=start_pos)
        self.speed = speed
        self.direction = pygame.math.Vector2(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]).normalize()

    def update(self):
        # Mover la bala hacia la dirección del clic
        self.rect.move_ip(self.direction * self.speed)

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
asteroid_images = ["asteroid1.png", "asteroid2.png", "asteroid3.png"]  # Asegúrate de tener imágenes de asteroides
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullet_speed = 8  # Ajusta la velocidad de la bala
bullet_length = 40  # Ajusta la longitud de la bala

while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Clic izquierdo
            bullet = Bullet((0, ALTO), event.pos, bullet_speed)
            bullets.add(bullet)

            # Crear otra bala desde (ANCHO, ALTO) hasta la posición del clic
            bullet2 = Bullet((ANCHO, ALTO), event.pos, bullet_speed)
            bullets.add(bullet2)

            # Verificar si se hizo clic en un asteroide
            clicked_asteroids = [asteroid for asteroid in asteroids if asteroid.rect.collidepoint(event.pos)]
            for clicked_asteroid in clicked_asteroids:
                asteroids.remove(clicked_asteroid)

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

    # Generar asteroides aleatorios cada ciertos frames
    if random.random() < 0.01:
        asteroid_image_path = random.choice(asteroid_images)
        asteroid = Asteroid(random.randint(0, ANCHO), random.randint(0, 420), asteroid_image_path)
        asteroids.add(asteroid)

    # Actualizar y dibujar los asteroides
    asteroids.update()

    # Actualizar y dibujar las balas
    bullets.update()

    screen.fill((0,0,0))

    # Dibujar líneas cortas para representar estrellas
    for star in stars:
        end_point = (int(star[0] + 8 * math.cos(star[2])), int(star[1] + 8 * math.sin(star[2])))
        pygame.draw.line(screen, white, (int(star[0]), int(star[1])), end_point, 2)

    # Dibujar y eliminar asteroides
    for asteroid in asteroids:
        screen.blit(asteroid.image, asteroid.rect.topleft)
        if not asteroid.growing:  # Eliminar asteroides que dejaron de crecer
            asteroids.remove(asteroid)

    # Dibujar y eliminar balas
    for bullet in bullets:
        bullet.update()
        end_pos = (bullet.rect.x + bullet.direction.x * bullet_length, bullet.rect.y + bullet.direction.y * bullet_length)
        pygame.draw.line(screen, (0, 255, 0), bullet.rect.topleft, end_pos, 5)  # Dibuja la bala como una línea

    points = [(0, 78), (194, 165), (189, 171), (0, 100)]
    pygame.draw.polygon(screen, grey, points)

    points = [(ANCHO, 78), (606, 165), (611, 171), (ANCHO, 100)]
    pygame.draw.polygon(screen, grey, points)

    pygame.draw.circle(screen, grey, (ANCHO//2, ALTO//2), 250, 8)

    points = [(-100, ALTO), (190, 433), (ANCHO//2, ALTO//2 + 120), (610, 433), (ANCHO + 100, ALTO)]
    pygame.draw.polygon(screen, dark_grey, points)

    points = [(70, ALTO), (200, 495), (ANCHO//2, ALTO//2 + 180), (595, 495), (ANCHO - 70, ALTO)]
    pygame.draw.polygon(screen, darker_grey, points)

    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    # Dibujar mira en pantalla
    screen.blit(mira.image, (mouse_x - mira.rect.width // 2, mouse_y - mira.rect.height // 2))

    pygame.display.flip()
    clock.tick(60)
