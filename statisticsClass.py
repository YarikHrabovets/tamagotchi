import pygame, os
from mainConst import screen, pixel_font

pygame.init()
clicked_statistics = False


class Statistics:
    def __init__(self, x, y, width, height, path, text_lg=None, text_name=None, text_days=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_lg = text_lg
        self.text_name = text_name
        self.text_days = text_days
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        self.exit = pygame.transform.scale(pygame.image.load('images/sprites/iconCross_beige.png'), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(75, 65))

        self.logika_image = pygame.transform.scale(pygame.image.load('images/sprites/logika.png'), (60, 60))

        self.logiki_text = pixel_font.render(self.text_lg, True, (255, 255, 255))
        self.logiki_text_rect = self.logiki_text.get_rect(center=(710, 75))

        self.name_text = pixel_font.render(self.text_name, True, (255, 255, 255))
        self.name_text_rect = self.name_text.get_rect(center=(400, 200))

        self.days_text = pixel_font.render(self.text_days, True, (255, 255, 255))
        self.days_text_rect = self.days_text.get_rect(center=(400, 250))

    def blit_statistics(self):
        if clicked_statistics:
            screen.blit(self.image, self.image_rect)
            screen.blit(self.logiki_text, self.logiki_text_rect)
            screen.blit(self.name_text, self.name_text_rect)
            screen.blit(self.days_text, self.days_text_rect)
            screen.blit(self.exit, self.exit_rect)
            screen.blit(self.logika_image, (620, 45))