import pygame, random
pygame.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
ubicaciones = [260,390]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/fondo.png").convert()
y = 0
def uploadBackground():
    # Fondo en movimiento
    global y
    y_relativa = y % background.get_rect().width
    screen.blit(background, (0,y_relativa - background.get_rect().height))
    if y_relativa < HEIGHT:
        screen.blit(background, (0,y_relativa))
    y += 5


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
            self.speed_x = +5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH-248:
            self.rect.right = WIDTH-248
        if self.rect.left < 264:
            self.rect.left = 264


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(obstacle_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(ubicaciones)
        self.rect.y = -50
        self.speedy = random.randrange(1 , 10)
        #self.speedx = random.randrange(-5, 5)

    def update(self):
        #self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT +10 or self.rect.left < -25 or self.rect.right >WIDTH +22:
            self.rect.x = random.choice(ubicaciones)
            self.rect.y = -50
            self.speedy = random.randrange(1,8)


obstacle_images = []
obstacle_list = ["assets/autoto.png",
                 "assets/autoto2.png",
                 "assets/milsim.png",
                 "assets/tonk.png",
                 "assets/motorola.png",
                 "assets/autobus.png"]

for img in obstacle_list:
    obstacle_images.append(pygame.image.load(img).convert())





all_sprites = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
car = Car()
all_sprites.add(car)

for i in range(4):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacle_list.add(obstacle)


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits = pygame.sprite.spritecollide(car, obstacle_list, False)
    if hits:
        # si el running esta en false cuando chocan se termina el juego
        running = True





    #screen.blit(background,[0,0])
    uploadBackground()
    all_sprites.draw(screen)
    pygame.display.flip()


pygame.quit()



































