import pygame, os
from mainConst import screen, pixel_font

pygame.init()


class Button:
    def __init__(self, x, y, width, height, path, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        self.normal_image = self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.btn_text = pixel_font.render(self.text, True, (255, 255, 255))
        self.btn_text_rect = self.btn_text.get_rect()
        self.btn_text_rect.center = self.rect.center

    def blit_btn(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.btn_text, self.btn_text_rect)

    def hover(self, x, y):
        if self.rect.collidepoint((x, y)):
            self.image = pygame.transform.scale(pygame.image.load('images/sprites/buttonLong_blue.png'), (self.width, self.height))
        else:
            self.image = self.normal_image