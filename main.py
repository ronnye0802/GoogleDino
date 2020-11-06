import pygame
import time as tm
from random import randint

pygame.init()

# Queste sono le sprite
dino = pygame.image.load('immagini/dino.png')
dino2 = pygame.image.load('immagini/dino2.png')
dino3 = pygame.image.load('immagini/dino3.png')
pavimento = pygame.image.load('immagini/pavimento.png')
cactus = pygame.image.load('immagini/Cactus.png')
cactus2 = pygame.image.load('immagini/Cactus2.png')
cactus3 = pygame.image.load('immagini/Cactus3.png')
cactus4 = pygame.image.load('immagini/Cactus4.png')
cactusGroup = pygame.image.load('immagini/CactusGroup.png')
cloud = pygame.image.load('immagini/cloud.png')
gameOver = pygame.image.load('immagini/gameover.png')

# Array con gli sprite
cammina = [dino, dino, dino, dino2, dino2, dino2, dino3, dino3, dino3]
ostacoli = [cactus, cactus2, cactus3, cactus4, cactusGroup]

# Costanti del gioco
clock = pygame.time.Clock()
last_time = tm.time()
SCHERMO = pygame.display.set_mode((600, 300))
pygame.display.set_caption("DinoGame! %d FPS" % clock.get_fps())
FPS = 60
FONT = pygame.font.SysFont('Comic Sans MS', 20, bold=False)

# Variabile booleana che per il main loop
running = True


class Cloud:
    def __init__(self):
        self.x = 650
        self.y = randint(10, 150)

    def generate(self):
        self.x -= AVANZ * dt
        SCHERMO.blit(cloud, (self.x, self.y))


# Classe Cactus
class Cactus:
    def __init__(self):
        self.x = 700
        self.y = randint(200, 210)
        self.rnd = randint(0, 4)

    def drawself(self):
        self.x -= AVANZ * dt
        SCHERMO.blit(ostacoli[self.rnd], (self.x, self.y))

    def collision(self, dino, dinox, dinoy):
        tollerance = 5
        dinodx = dinox + dino.get_width() - tollerance
        dinosx = dinox + tollerance
        cactusdx = self.x + ostacoli[self.rnd].get_width()
        cactussx = self.x
        dinoup = dinoy - tollerance
        dinodown = dinoy + dino.get_height() - tollerance
        cactusup = self.y
        cactusdown = self.y - 5
        if self.x <= -10:
            cacti.remove(self)
        if dinodx > cactussx and dinosx < cactusdx:
            if dinoup < cactusup and dinodown > cactusdown:
                gameover()


# Inizializzo le variabili globali
def initialize():
    global dinox, dinoy, dinovely, jumping
    global pavx, pavy, pavx2, pavy2
    global walkpoint
    global cacti
    global score, time
    global DIFF
    global clouds
    global AVANZ
    # DIFF = pygame.event.Event(DIFF)
    # pygame.time.set_timer(DIFF, 10000)
    dinox, dinoy, dinovely, jumping = 70, 200, 0, False
    pavx, pavy = 0, 235
    walkpoint = 0
    AVANZ = 4
    cacti = [Cactus()]
    clouds = [Cloud()]
    score, time = 0, 0


# Chiamo la funzione inizializza
initialize()


# Definisco una funzione che aggiorna ogni frame lo schermo
def draw():
    SCHERMO.fill((255, 255, 255))
    SCHERMO.blit(pavimento, (pavx, pavy))
    SCHERMO.blit(pavimento, (pavx + 1200, pavy))
    for c in cacti:
        c.drawself()
    for i in clouds:
        i.generate()
    SCHERMO.blit(cammina[walkpoint], (dinox, dinoy))
    scoreRender = FONT.render(str(int(score)), 1, (0, 0, 0))
    SCHERMO.blit(scoreRender, (450, 10))


# Qui definisco una funzione per creare un "timer" che manda avanti il gioco definendo i "Tick" del gioco
def update():
    pygame.display.update()
    clock.tick(FPS)


def gameover():
    SCHERMO.blit(gameOver, (200, 150))
    update()
    dead = True
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initialize()
                dead = False
            if event.type == pygame.QUIT:
                running = False
                dead = False
                quit()


# Main loop del gioco, dove avvengono la maggior parte dei calcoli
while running:
    dt = tm.time() - last_time
    dt *= 60
    last_time = tm.time()

    score += 0.166
    time += 0.016
    pavx -= AVANZ * dt

    if pavx <= -1200:
        pavx = 0

    if time > 20:
        time = 0
        AVANZ += 1
    if dinoy >= 200:
        jumping = False
        dinoy = 200
        dinovely = 0
    if jumping and dinoy <= 120:
        dinovely += 1 * dt
        walkpoint = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not jumping:
                jumping = True
                dinovely = -10 * dt

        if event.type == pygame.QUIT:
            running = False

    dinoy += dinovely

    if walkpoint > 8:
        walkpoint = 0

    if cacti[-1].x < randint(-10, 200):
        cacti.append(Cactus())
        if cacti[-1].x < -10:
            cacti.pop(-2)
    if clouds[-1].x < -10:
        clouds.pop(-2)
    if clouds[-1].x < randint(200, 300):
        clouds.append(Cloud())

    for c in cacti:
        c.collision(dino, dinox, dinoy)

    draw()
    walkpoint += 1
    update()

# In caso si clicchi la X per uscire dal gioco viene chiamato il method quit()
def quit():
    pygame.quit()
