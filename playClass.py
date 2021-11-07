import pygame, os
import time
from mainConst import action, tamagotchiJump, pixel_font, screen
from abs_path import abs_path

pygame.init()

animCount = 0
timeCount = 60
scoreCount = 0
seconds = 1
clicked_play = False


class Play:
    def __init__(self):
        self.x = 325
        self.y = 400
        self.width = 150
        self.height = 150
        self.background_anim = [pygame.transform.scale(pygame.image.load(abs_path('images/background/background-0.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(abs_path('images/background/background-1.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(abs_path('images/background/background-2.png')), (800, 500)),
                                pygame.transform.scale(pygame.image.load(abs_path('images/background/background-3.png')), (800, 500))]
        self.exit = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/iconCross_beige.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(40, 40))

    def blit_play(self):
        global animCount
        if clicked_play:
            if animCount + 1 >= len(self.background_anim) * 7:
                animCount = 0
                screen.blit(self.background_anim[0], (0, 0))
                screen.blit(tamagotchiJump[0], (self.x, self.y))
            else:
                screen.blit(self.background_anim[animCount // 7], (0, 0))
                screen.blit(tamagotchiJump[animCount // 7], (self.x, self.y))
                animCount += 1

        time_left = pixel_font.render(f'Time Left: {timeCount}', True, (255, 255, 255))
        score = pixel_font.render(f'Score: {scoreCount}', True, (255, 255, 255))
        screen.blit(score, (600, 20))
        screen.blit(time_left, (600, 60))
        screen.blit(self.exit, self.exit_rect)

    def check_time(self, game_time):
        global clicked_play, timeCount, scoreCount, seconds
        t_time = time.time() - game_time
        if seconds < t_time:
            timeCount -= 1
            seconds += 1
        if timeCount == 0:
            action['logiki'] += scoreCount // 2
            if action['happy'] + 15 > 100:
                score = 100 - action['happy']
                action['happy'] += score
            else:
                action['happy'] += 15
            action['satiety'] -= 2
            clicked_play = False
            timeCount = 60
            seconds = 1
            scoreCount = 0
            pygame.mixer.music.unload()
            pygame.mixer.music.load(abs_path('sounds/backgroundMusic.ogg'))
            pygame.mixer.music.play(loops=-1)

    def control(self, keys):
        if keys[pygame.K_LEFT] and self.x > 1:
            self.x -= 7
        if keys[pygame.K_RIGHT] and self.x < 800 - self.width:
            self.x += 7


class Basket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.basket = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/basket.png')), (150 // 2, 150 // 3))
        self.rect = self.basket.get_rect(center=(400, 440))

    def blit_basket(self):
        screen.blit(self.basket, self.rect)

    def control(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 35:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT] and self.rect.x < 690:
            self.rect.x += 7


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, speed, filename, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename), (30, 30))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self, height):
        if self.rect.y < height - 20:
            self.rect.y += self.speed
        else:
            self.kill()
