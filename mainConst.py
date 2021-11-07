import pygame, os

pygame.init()

width = 150
height = 150
action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'logiki': 50}
screen = pygame.display.set_mode((800, 500))
pixel_font = pygame.font.Font('font/technicality1.ttf', 27)
tamagotchiJump = [pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-0.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-1.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-2.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-3.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-4.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-5.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-6.png'), (width, height)),
                  pygame.transform.scale(pygame.image.load('images/sprites/tamagotchi animation/tamagotchi-7.png'), (width, height))]