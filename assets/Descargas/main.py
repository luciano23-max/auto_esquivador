# !!!version del juego que hice antes de asistir a la clase, 
# cumple la funcionalidad especificada en la letra



# juego de disparos en pygame
# se asume que los assets están adentro de una carpeta llamada "assets" adentro de la misma carpeta del script

# funcionalidad:
# * pantalla de bienvenida
# * pantalla de fin si se llega a la puntuacion final
# * pantalla de pausa
# * disparar con el clic izquierdo o con la tecla espacio
# * mover la nave con las teclas A/D o flechas izquierda/derecha
# * F3 para mostrar/ocultar colisiones (alternar debug = False o True)
# * colisiones entre la nave y los meteoros, y entre las balas y los meteoros
# * explosion al chocar con un meteoro; daño a la nave
# * barra de escudo que se va reduciendo al chocar con meteoros (4 impactos antes de perder)
# * puntaje que aumenta al destruir meteoros
# * combos de explosiones (y en consecuencia explosiones en cadena) con la EXPLOSION_EXPLOTA = True/False
# * EXPLOSION_EXPLOSIVA = True hace que las explosiones dañe la nave

# nota: aumentar los FPS hace todo mas rapido y requiere mas concentración, y viceversa,
#  habilitar EXPLOSION_EXPLOTA = True hace que defender la nave sea mas fácil y se ganen puntos mas rapido

import pygame, random, sys, os

# inicializar 
pygame.init(); pygame.display.set_caption("juegardo")
reloj = pygame.time.Clock()

# colores y assets
ANCHO = 800; ALTO = 600; pantalla = pygame.display.set_mode((ANCHO, ALTO))            # pantalla
NEGRO = (0, 0, 0); BLANCO = (255, 255, 255); ROJO = (255, 0, 0); VERDE = (0, 255, 0)  # colores
ASSETS = os.path.join("assets")                                                       # assets (asume que están adentro de una carpeta llamada "assets" adentro de la misma carpeta del script)

# para configurar 
debug = False                # mostrar colisiones (variable pq puede cambiar en ejecución)
vol = 0.4                    # volumen del sonido (variable pq puede cambiar en ejecución)
FIN = True                   # if True, el juego termina a una cierta puntuación (FINAL) y se muestra la pantalla de fin
FINAL = 1000                 # puntuación a la que se termina el juego (si FIN = True)
VEL_BALA = -10               # <- para modificar la velocidad de la bala
FPS = 60                     # <- para modificar los fps (c usa en el loop principal) (es la velocidad del juego)
EXPLOSION_EXPLOTA = True    # if True, hace que la explosión en sí colisione con los meteoros y los destruya (se pueden hacer combos) no sabía si agregarlo asi que es una opción. logica: tambien hay colision entre los meteoros y las explosiones. consecuencia no esperada: hay explosiones en cadena si varios meteoros se superponen
EXPLOSION_EXPLOSIVA = False  # if True, hace que la explosion también colisione con la nave y le haga daño (-1 d escudo) también opcional
MAX_METEOROS = 10            # numero maximo de meteoros simultáneamente en pantalla

# assets:
FONDO = pygame.image.load(os.path.join(ASSETS, "background.png")).convert()       # fondo
IMG_NAVE = pygame.image.load(os.path.join(ASSETS, "player.png")).convert_alpha()  # navesita
IMG_LASER = pygame.image.load(os.path.join(ASSETS, "laser1.png")).convert_alpha() # bala
IMAGENES_METEOROS = [pygame.image.load(os.path.join(ASSETS, f"meteorGrey_big{i}.png"  )).convert_alpha() for i in range(1, 5)] + \
                    [pygame.image.load(os.path.join(ASSETS, f"meteorGrey_med{i}.png"  )).convert_alpha() for i in range(1, 3)] + \
                    [pygame.image.load(os.path.join(ASSETS, f"meteorGrey_small{i}.png")).convert_alpha() for i in range(1, 3)] + \
                    [pygame.image.load(os.path.join(ASSETS, f"meteorGrey_tiny{i}.png ")).convert_alpha() for i in range(1, 3)] # linea partida en 3: cargar los meteoros y convertir canal alpha (png)
EXPLOSIONES = [pygame.image.load(os.path.join(ASSETS, f"regularExplosion0{i}.png")).convert_alpha() for i in range(9)]
SONIDO_LASER = pygame.mixer.Sound(os.path.join(ASSETS, "laser5.ogg"))        # sonido d disparar
SONIDO_EXPLOSION = pygame.mixer.Sound(os.path.join(ASSETS, "explosion.wav")) # sonido d explosion
# reproducir musica
pygame.mixer.music.load(os.path.join(ASSETS, "music.ogg")); pygame.mixer.music.play(-1) 
#texto:
pygame.font.init(); FUENTE = pygame.font.SysFont("Arial", 24); FUENTE_2 = pygame.font.SysFont("Arial", 20)

# puntaje y escudo
puntuacion = 0; escudo = 4 # valores por defecto

# nave
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_NAVE  # agarrar asset
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2; self.rect.bottom = ALTO - 10 # posicion inicial
        self.velocidad = 10 # velocidad

    def update(self):   # movimiento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

# bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMG_LASER  # agarrar asset
        self.rect = self.image.get_rect()
        self.rect.centerx = x; self.rect.bottom = y # posicion inicial
        self.velocidad = VEL_BALA # movimiento simple

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

# meteoro
class Meteoro(pygame.sprite.Sprite):
    def __init__(self): # spawnear
        super().__init__()
        self.image = random.choice(IMAGENES_METEOROS) # agarrar asset
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width); self.rect.y = random.randint(-150, -50) # posicion random
        self.velocidad_y = random.randint(1, 5); self.velocidad_x = random.randint(-2, 2) # velocidad random

    def update(self): # funcionalidad movimiento
        self.rect.y += self.velocidad_y; self.rect.x += self.velocidad_x
        if self.rect.top > ALTO or self.rect.left < -100 or self.rect.right > ANCHO + 100: # si c va de la pantalla
            self.rect.x = random.randint(0, ANCHO - self.rect.width); self.rect.y = random.randint(-150, -50) # respawn random
            self.velocidad_y = random.randint(1, 5); self.velocidad_x = random.randint(-2, 2) # respawn con velocidadrandom

# explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, centro): # spawnear
        super().__init__()
        self.frames = EXPLOSIONES
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = centro
        self.tiempo_ultima_actualizacion = pygame.time.get_ticks(); self.fps = 60

    def update(self): # funcionalidad (existir)
        ahora = pygame.time.get_ticks() # q hora es?
        if ahora - self.tiempo_ultima_actualizacion > 1000 // self.fps:
            self.tiempo_ultima_actualizacion = ahora    # actualizar:
            self.frame_index += 1                       # siguiente frame
            if self.frame_index == len(self.frames):
                self.kill()                             # killear la explosion al llegar al ultimo frame de su animacion
            else:
                centro = self.rect.center
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = centro

# elementos del juego
todos_los_sprites = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
balas = pygame.sprite.Group()
explosiones_activas = pygame.sprite.Group()
JUGADOR = Nave()
# spawn de la nave
todos_los_sprites.add(JUGADOR) # la nave -> al grupo d sprites

for _ in range(MAX_METEOROS):      # crear meteoros iniciales
    meteoro = Meteoro()
    todos_los_sprites.add(meteoro)
    meteoritos.add(meteoro)

def mutear():
    vol = 0; vol_sonidos = 0; pygame.mixer.music.set_volume(vol); ajustar_volumen_sonidos(vol_sonidos)

def mostrar_pantalla_bienvenida():  # pantalla de bienvenida
    pantalla.blit(FONDO, (0, 0)) # poner fondo
    TITULO = FUENTE.render("Shooter", True, BLANCO) # textos
    CREADOR = FUENTE.render("Creado por Leandro Testa", True, BLANCO)
    INICIAR = FUENTE.render("Presiona cualquier tecla para comenzar", True, BLANCO)
    CONTROLES = FUENTE_2.render("Movimiento: A/D o ←/→, Disparar: espacio o click izquierdo", True, BLANCO)
    CONTROLES_VOL = FUENTE_2.render("Rueda del ratón para cambiar el volumen", True, BLANCO)
    SALIR_MOSTRARCOLISIONES = FUENTE_2.render("F4 para salir, F3 para mostrar colisiones de los objetos", True, BLANCO)
    pantalla.blit(INICIAR, (ANCHO // 2 - INICIAR.get_width() // 2, ALTO // 3 + 150))
    pantalla.blit(CONTROLES, (ANCHO // 2 - CONTROLES.get_width() // 2, ALTO // 3 + 200))
    pantalla.blit(CONTROLES_VOL, (ANCHO // 2 - CONTROLES.get_width() // 3, ALTO // 3 + 250))
    pantalla.blit(SALIR_MOSTRARCOLISIONES, (ANCHO // 2 - SALIR_MOSTRARCOLISIONES.get_width() // 2, ALTO // 2 + 200))
    pantalla.blit(TITULO, (ANCHO // 2 - TITULO.get_width() // 2, ALTO // 6))    # dibujar textos
    pantalla.blit(CREADOR, (ANCHO // 2 - CREADOR.get_width() // 2, ALTO // 5 + 50))

    pygame.display.flip() # updatear la pantalla

    esperando = True;   # esperar a que el usuario de algun input
    while esperando:
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
mostrar_pantalla_bienvenida()

def mostrar_pantalla_pausa():
    pantalla.blit(FONDO, (0, 0)) # poner fondo
    titulop = FUENTE.render("Pausa", True, BLANCO) # poner textos
    textp = FUENTE.render("Presiona cualquier tecla para reanudar", True, BLANCO)
    pantalla.blit(titulop, (ANCHO // 2 - titulop.get_width() // 2, ALTO // 3))  # dibujar texto
    pantalla.blit(textp, (ANCHO // 2 - textp.get_width() // 2, ALTO // 3 + 50))

pantalla.fill(NEGRO); pygame.display.flip() # limpiar pantalla

def ajustar_volumen_sonidos(volumen): # ruedita del mouse ajusta el sonido de todo no solo la musica
    SONIDO_LASER.set_volume(volumen)
    SONIDO_EXPLOSION.set_volume(volumen)
vol_sonidos = 0.4; ajustar_volumen_sonidos(vol_sonidos)

def mostrar_pantalla_final():
    pantalla.blit(FONDO, (0, 0)) # poner fondo
    TITULO = FUENTE.render("Shooter", True, BLANCO) # textos
    CREADOR = FUENTE.render("Creado por Leandro Testa", True, BLANCO)
    CONTINUAR = FUENTE.render("Presiona cualquier tecla para resetear", True, BLANCO)
    GANASTE = FUENTE.render(f"¡Ganaste! Llegaste a " + str(FINAL) + " puntos", True, BLANCO)
    pantalla.blit(TITULO, (ANCHO // 2 - TITULO.get_width() // 2, ALTO // 6))    # dibujar textos
    pantalla.blit(CREADOR, (ANCHO // 2 - CREADOR.get_width() // 2, ALTO // 5 + 50))
    pantalla.blit(CONTINUAR, (ANCHO // 2 - CONTINUAR.get_width() // 2, ALTO // 2))
    pantalla.blit(GANASTE, (ANCHO // 2 - GANASTE.get_width() // 2, ALTO // 3 + 50))

    pygame.display.flip()
    esperando = True
    while esperando:
        reloj.tick(FPS)
        mutear()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False
                vol = 0.4; vol_sonidos = 0.4; pygame.mixer.music.set_volume(vol); ajustar_volumen_sonidos(vol_sonidos) # desmutear

def mostrar_pantalla_perdiste():
    PERDISTE = FUENTE.render("perdiste :c", True, BLANCO)
    pantalla.blit(PERDISTE, (ANCHO // 2 - PERDISTE.get_width() // 2, ALTO // 3))
    pygame.display.flip() # updatear la pantalla


# loop principal del juego:
ejecutando = True; pausado = False; 
while ejecutando:
    reloj.tick(FPS); # por defecto 60
    pygame.mixer.music.set_volume(vol)
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_F3:
                debug = not debug           # F3 alterna debug
            elif evento.key == pygame.K_F4:
                ejecutando = False          # quitear
            elif evento.key == pygame.K_ESCAPE:
                pausado = not pausado
        if not pausado: # manejar el resto d cosas solo si no pausado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bala = Bala(JUGADOR.rect.centerx, JUGADOR.rect.top) # poner bala arriba de la nave
                    todos_los_sprites.add(bala)
                    balas.add(bala)
                    SONIDO_LASER.play()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    bala = Bala(JUGADOR.rect.centerx, JUGADOR.rect.top) # poner bala arriba de la nave
                    todos_los_sprites.add(bala)
                    balas.add(bala)
                    SONIDO_LASER.play()
            elif evento.type == pygame.MOUSEWHEEL:
                vol += evento.y/10; vol_sonidos += evento.y/10
            elif evento.type == pygame.QUIT: # if para cerrar el juego
                ejecutando = False
    
    if FIN and puntuacion >= FINAL: # si se llega a la puntuacion final,
        mostrar_pantalla_final()    # se muestra la pantalla de fin
        puntuacion = 0; escadudo = 4 # reiniciar puntaje y escudo

    if pausado:     # funcionalidad de pausa
        mostrar_pantalla_pausa(); pygame.display.flip()
        pygame.mixer.music.set_volume(0)
        if evento.type == pygame.QUIT: # permitir cerrar el juego en pausa
            ejecutando = False
        continue

    todos_los_sprites.update()

    colisiones = pygame.sprite.groupcollide(meteoritos, balas, True, True); # colisiones entre meteoritos y balas
    for colision in colisiones:
        puntuacion += 1
        SONIDO_EXPLOSION.play()                # sonido explosion
        expl = Explosion(colision.rect.center) # explosion
        todos_los_sprites.add(expl)            # explosion es sprite
        explosiones_activas.add(expl)
        meteoro = Meteoro()                    # reponer el meteoro
        todos_los_sprites.add(meteoro)         # meteoro es sprite
        meteoritos.add(meteoro)                # meteoro es sprite

    if EXPLOSION_EXPLOTA:
        colisiones_explosiones = pygame.sprite.groupcollide(meteoritos, explosiones_activas, True, True); # colisiones entre meteoritos y explosiones OPCIONAL: ExplosionExplota = True
        for colision in colisiones_explosiones:
            puntuacion += 1
            SONIDO_EXPLOSION.play()                # sonido explosion
            expl = Explosion(colision.rect.center) # explosion
            todos_los_sprites.add(expl)            # explosion es sprite
            explosiones_activas.add(expl)
            meteoro = Meteoro()                    # reponer el meteoro
            todos_los_sprites.add(meteoro)         # meteoro es sprite
            meteoritos.add(meteoro)                # meteoro es sprite

    if EXPLOSION_EXPLOSIVA:
        colisiones_explosiones_nave = pygame.sprite.spritecollide(JUGADOR, explosiones_activas, True); # colisiones entre la nave y las explosiones OPCIONAL: AutoDaño = True
        for colision in colisiones_explosiones_nave:
            SONIDO_EXPLOSION.play()
            escudo -= 1                             # daño
            exlp = Explosion(colision.rect.center)  # explosion consecuente

    choques = pygame.sprite.spritecollide(JUGADOR, meteoritos, True)  # colisiones entre meteoritos y nave
    for choque in choques:
        escudo -= 1  # daño
        SONIDO_EXPLOSION.play()
        expl = Explosion(choque.rect.center)
        todos_los_sprites.add(expl)
        explosiones_activas.add(expl)
        # reponer el meteoro
        meteoro = Meteoro()
        todos_los_sprites.add(meteoro)
        meteoritos.add(meteoro)

    if escudo <= 0:  # verificar si el escudo se agotó
        pygame.time.wait(250)  # esperar 250ms para que no sea muy instantaneo
        mostrar_pantalla_perdiste()  # mostrar pantalla de "perdiste"
        mutear(); pygame.time.wait(2000)  # mutear y esperar 2 segundos antes de cerrar
        pantalla.fill(NEGRO); pygame.time.wait(500) # limpiar
        ejecutando = False  # cerrar

    pantalla.blit(FONDO, (0, 0))     # dibujar fondo
    todos_los_sprites.draw(pantalla) # dibujar todos los sprites diferidamante (a veces se bugueaban y no se mostraban)

    # puntos y escudo
    TEXTO_PUNTUACION = FUENTE.render(f"Puntos: {puntuacion}", True, BLANCO)
    pantalla.blit(TEXTO_PUNTUACION, (10, 10))
    TEXTO_ESCUDO = FUENTE.render("Escudo:", True, BLANCO)
    pantalla.blit(TEXTO_ESCUDO, (10, 40))

    # dibujar puntos y escudo
    BARRA_X = 100; BARRA_Y = 45
    pygame.draw.rect(pantalla, ROJO, (BARRA_X, BARRA_Y, 100, 10)) # dibujar barra (roja)
    ancho_escudo = max(0, int(100 * escudo / 4)) # porcentaje de la barra verde (del escudo)
    pygame.draw.rect(pantalla, VERDE, (BARRA_X, BARRA_Y, ancho_escudo, 10)) # dibujar barra verde arriba de la roja

    if debug: # mostrar colisiones
        for sprite in todos_los_sprites:
            pygame.draw.rect(pantalla, (0, 255, 0), sprite.rect, 1)

    pygame.display.flip()
pygame.quit(); sys.exit()