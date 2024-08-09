import sys

import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, img):
        super().__init__()
        self.img = img
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.img, self.rect)


player = Soldier(200, 200, 3, pygame.image.load("img/player/idle/0.png"))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    player.draw()

    pygame.display.update()

pygame.quit()
sys.exit()
