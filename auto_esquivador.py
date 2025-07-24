import pygame, random

pygame.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/fondo.png").convert()
y = 0

# Carriles (ubicaciones X)
ubicaciones_pos = {
    "izquierda": 290,
    "derecha": 435
}

# Tiempo mínimo entre apariciones por carril
INTERVALO_MS = 1000
tiempos_ultima_aparicion = {
    "izquierda": 0,
    "derecha": 0
}

explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

obstacle_images = []
obstacle_paths = [
    "assets/autoto.png",
    "assets/autoto2.png",
    "assets/milsim.png",
    "assets/tonk.png",
    "assets/motorola.png",
    "assets/autobus.png"
]
for img in obstacle_paths:
    obstacle_images.append(pygame.image.load(img).convert())


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/prota2.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH - 248:
            self.rect.right = WIDTH - 248
        if self.rect.left < 264:
            self.rect.left = 264

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, ubicacion_label):
        super().__init__()
        self.image = random.choice(obstacle_images).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.ubicacion = ubicacion_label
        self.rect.x = ubicaciones_pos[ubicacion_label]
        self.rect.y = -100
        self.speedy = random.randint(8, 10)
        self.activo = True

    def reset(self):
        self.rect.y = -100
        self.speedy = random.randint(8, 10)
        self.image = random.choice(obstacle_images)
        self.image.set_colorkey(BLACK)
        self.activo = True
        tiempos_ultima_aparicion[self.ubicacion] = pygame.time.get_ticks()

    def update(self):
        if self.activo:
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.activo = False  # Se sale, se apaga y espera su momento

class Explosion(pygame.sprite.Sprite):
    def __init__(self, centre):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                centre = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = centre

def uploadBackground():
    global y
    y_relativa = y % background.get_rect().width
    screen.blit(background, (0, y_relativa - background.get_rect().height))
    if y_relativa < HEIGHT:
        screen.blit(background, (0, y_relativa))
    y += 5

def manejar_aparicion_obstaculos():
    tiempo_actual = pygame.time.get_ticks()
    for obstaculo in obstacle_list:
        if not obstaculo.activo:
            tiempo_ultimo = tiempos_ultima_aparicion[obstaculo.ubicacion]
            if tiempo_actual - tiempo_ultimo >= INTERVALO_MS:
                obstaculo.reset()

# Grupos
all_sprites = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
car = Car()
all_sprites.add(car)

# Crear un obstáculo por carril (2 total)
for ubicacion in ubicaciones_pos:
    obstaculo = Obstacle(ubicacion)
    obstacle_list.add(obstaculo)
    all_sprites.add(obstaculo)

# Main loop
running = True
while running:
    clock.tick(60)
    manejar_aparicion_obstaculos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Colisiones con jugador
    hits = pygame.sprite.spritecollide(car, obstacle_list, False)
    if hits:
        running = True

    # Fondo y dibujado
    uploadBackground()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()



















