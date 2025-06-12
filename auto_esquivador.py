import pygame, random
pygame.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/Gemini_Generated_Image_43m9ik43m9ik43m91.png").convert()
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
        self.image = pygame.image.load("assets/auto0.png").convert()
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
        if self.rect.right > WIDTH-170:
            self.rect.right = WIDTH-170
        if self.rect.left < 170:
            self.rect.left = 170


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(obstacle_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH -self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1 , 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT +10 or self.rect.left < -25 or self.rect.right >WIDTH +22:
            self.rect.x = random.randrange(WIDTH -self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)





















all_sprites = pygame.sprite.Group()
car = Car()
all_sprites.add(car)


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()

    #screen.blit(background,[0,0])
    uploadBackground()
    all_sprites.draw(screen)
    pygame.display.flip()


pygame.quit()



































