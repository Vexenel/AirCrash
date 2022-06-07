# Импортируем
import pygame
import sys
import random
import time


# Подготавливаем к работе
pygame.init()


# Настройка фпс
FPS = 60
FramePerSec = pygame.time.Clock()

# Создание цветов
BLUE = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настройка переменных
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1698
SPEED = 20
SCORE = 0


# Настройка шрифтов
font = pygame.font.SysFont("Chilanka", 100)
font_small = pygame.font.SysFont("Chilanka", 50)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("sky.png")


# Создание экрана и название экрана
DISPLAYSURF = pygame.display.set_mode((1200, 1698))
pygame.display.set_caption("Airplane Game")


# Создание классов
# Создание класса врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("en.png")
        self.rect = self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-100, -100)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 1200):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Создание класcа игрока
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ap.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_key[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)

        if self.rect.left > 0:
            if pressed_key[pygame.K_LEFT]:
                self.rect.move_ip(-10, 0)
            if pressed_key[pygame.K_RIGHT]:
                self.rect.move_ip(10, 0)


P1 = Player()
E1 = Enemy()

# Cоздали группу врагов
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Добавление ивентов
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Создание цикла
while True:

    # Перебираем все события
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

# Перемещаем и перерисовавыем
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

# Что происходит при столкновении
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('tc.mp3').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (270, 400))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
