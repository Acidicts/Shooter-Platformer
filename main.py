import os
import sys

import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

all_sprites = pygame.sprite.Group()


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, frames, groups=None):
        super().__init__(groups)
        self.scale = scale
        self.frames, self.frame_index = frames, 0
        self.img = self.frames[self.frame_index]
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
        self.img_n = self.img
        self.img_f = pygame.transform.flip(self.img, True, False)

        self.rect = self.img.get_frect()
        self.rect.center = (x, y)

        self.direction = pygame.math.Vector2(0, 0)

    def draw(self, offset):
        rect = self.rect.x + offset[0], self.rect.y + offset[1]
        if int(self.direction.x) == 1:
            self.img = self.img_n
        elif int(self.direction.x) == -1:
            self.img = self.img_f

        screen.blit(self.img, rect)

    def animate(self, dt):
        self.frame_index += 10 * dt
        img = self.frames[int(self.frame_index) % len(self.frames)]
        img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.img_n = img
        self.img_f = pygame.transform.flip(img, True, False)

    def update(self, dt, offset):
        self.animate(dt)
        self.draw(offset)


class Enemy(Soldier):
    def __init__(self, x, y, scale, img, groups, speed):
        super().__init__(x, y, scale, img, groups)
        if speed > 0:
            self.direction.x = 1
        elif speed < 0:
            self.direction.x = -1
            speed = -speed
        self.speed = speed

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt

    def update(self, dt, offset):
        self.move(dt)
        self.draw(offset)
        self.animate(dt)


class Player(Soldier):
    def __init__(self, x, y, scale, frames, groups):
        super().__init__(x, y, scale, frames, groups)

        self.direction = pygame.math.Vector2(0, 0)

    def draw(self, offset):
        screen.blit(self.img, self.rect)

    def update(self, dt, offset):
        self.draw(offset)
        self.animate(dt)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, direction):
        super().__init__(groups)
        self.image = pygame.Surface((4, 2))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, dt, offset):
        self.rect.x += 500 * dt * self.direction
        self.rect.x -= offset.x
        if self.rect.collidelist(all_sprites.sprites()) >= 0 and not self.rect.colliderect(player.rect):
            self.kill()


def load_animation(path):
    frames = []
    for i in os.listdir(path):
        img = pygame.image.load(f"{path}{i}")
        frames.append(img)
    return frames


# noinspection PyTypeChecker
player = Player(200, 200, 3, load_animation('img/player/idle/'), all_sprites)
# noinspection PyTypeChecker
enemy = Enemy(400, 200, 3, load_animation('img/enemy/idle/'), all_sprites, -200)

run = True
clock = pygame.time.Clock()

offset = pygame.math.Vector2(0, 0)

bullets = []

while run:
    dt = clock.tick() / 1000
    pygame.display.set_caption("Shooter FPS : " + str(round(clock.get_fps())))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.centerx, player.rect.centery, all_sprites, player.direction.x))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        offset.x += 400 * dt
    if keys[pygame.K_d]:
        offset.x -= 400 * dt

    screen.fill((144, 201, 120))

    all_sprites.update(dt, offset)

    pygame.display.update()

pygame.quit()
sys.exit()
