import random
import os
import time
import pygame
import foodClass
import panelClass
import playClass
import statisticsClass
from buttonClass import Button
from mainConst import action, tamagotchiJump, pixel_font
from abs_path import abs_path

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)
day = 90000
daysCount = 0
daysEvent = pygame.USEREVENT + 1
pygame.time.set_timer(daysEvent, day)

screen_width = 800
screen_height = 500
FPS = 45
timeout = 15
animCount = 0
text_timer = 0
night_timer = 0
endMenu = False
endGame = False
isSleep = False
cantClear = False
cantHelp = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tamagotchi')
pygame.display.set_icon(pygame.image.load(abs_path('images/sprites/logika.ico')))
clock = pygame.time.Clock()
start_time = None
game_time = None

cursor = pygame.image.load(abs_path('images/sprites/cursorHand_blue.png'))
pygame.mouse.set_visible(False)
background_menu = [pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/gifMenu-0.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/gifMenu-1.png')), (screen_width, screen_height))]
background = pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/background.jpg')), (screen_width, screen_height))
gameover_img = pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/gameover_1.png')), (screen_width, screen_height))
sleep_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites//sleep.png')), (50, 50))
day_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/day.png')), (50, 50))
night_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/night.png')), (50, 50))
gameover_text = pixel_font.render('If you want play one more time, you have to restart game', True, (75, 255, 255))


def tamagotchiAnimation(x, y):
    global animCount
    if not isSleep:
        if animCount + 1 >= len(tamagotchiJump) * 6:
            animCount = 0
            screen.blit(tamagotchiJump[0], (x, y))
        else:
            screen.blit(tamagotchiJump[animCount // 6], (x, y))
            animCount += 1

        screen.blit(day_image, (735, 70))
    else:
        screen.blit(tamagotchiJump[0], (x, y))


def scoreTick():
    global start_time, timeout
    t_time = time.time() - start_time
    if t_time > timeout:
        action['satiety'] -= 3
        action['toilet'] -= 2
        action['happy'] -= 3
        action['health'] -= random.randint(0, 5)
        start_time = time.time()


def clearAfter():
    global cantClear
    if action['toilet'] + 16 <= 100:
        action['toilet'] += 16
        toilet_sound = pygame.mixer.Sound(abs_path('sounds/toilet.ogg'))
        toilet_sound.play()
    else:
        cantClear = True


def medicine():
    global cantHelp
    if action['logiki'] - 3 >= 0:
        if action['health'] + 10 <= 100:
            action['health'] += 10
            action['logiki'] -= 3
            medicine_sound = pygame.mixer.Sound(abs_path('sounds/medicine.ogg'))
            medicine_sound.play()
        else:
            cantHelp = True


def gameOver():
    if action['satiety'] <= 0 or action['toilet'] <= 0 or action['happy'] <= 0 or action['health'] <= 0:
        pygame.mixer.music.stop()
        screen.blit(gameover_img, (0, 0))
        screen.blit(gameover_text, (35, 450))


def spawn_coin(group):
    return playClass.Coin(random.randint(40, 760), random.randint(3, 5), abs_path('images/sprites/coin.png'), group)

coins = pygame.sprite.Group()

help_menu = panelClass.Panel(400, 250, 750, 450, abs_path('images/sprites/panel_brown.png'), ' You have to keep the indicators normal.',
                             'If at least one of them is equal to zero, you will lose.', 'Good Luck!')

logika_label = Button(70, 60, 100, 100, abs_path('images/sprites/logika.png'))
start_btn = Button(140, 150, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Start')
rule_btn = Button(140, 250, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Help')
exit_btn = Button(140, 350, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Exit')


info_satiety = Button(20, 30, 25, 50, abs_path('images/sprites/lightning.png'))
info_toilet = Button(150, 30, 50, 50, abs_path('images/sprites/toilet.png'))
info_happy = Button(270, 30, 50, 50, abs_path('images/sprites/smile.png'))
info_health = Button(30, 90, 60, 60, abs_path('images/sprites/health.png'))

btn_statistic = Button(715, 40, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Statistic')

btn_satiety = Button(85, 467, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Feed')
btn_toilet = Button(285, 467, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Clear')
btn_play = Button(515, 467, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Play')
btn_health = Button(715, 467, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Medicine')

food = foodClass.FoodMenu(400, 250, 750, 450, abs_path('images/sprites/panel_brown.png'),
                          abs_path('images/sprites/buttonSquare_beige_pressed.png'),
                          abs_path('images/sprites/food_1.png'), abs_path('images/sprites/food_2.png'), abs_path('images/sprites/food_3.png'))

play = playClass.Play()
basket = playClass.Basket()


button_sound = pygame.mixer.Sound(abs_path('sounds/button.ogg'))
button_sound.set_volume(0.05)


def game():
    global endGame, isSleep, daysCount, night_timer, text_timer, cantClear, cantHelp, game_time, start_time
    start_time = time.time()
    pygame.mixer.music.load(abs_path('sounds/backgroundMusic.ogg'))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    while not endGame:
        screen.blit(background, (0, 0))
        info_satiety.blit_btn()
        satiety_text = pixel_font.render(str(action['satiety']), False, (255, 255, 255))
        screen.blit(satiety_text, (40, 15))
        info_toilet.blit_btn()
        toilet_text = pixel_font.render(str(action['toilet']), False, (255, 255, 255))
        screen.blit(toilet_text, (180, 15))
        info_happy.blit_btn()
        smile_text = pixel_font.render(str(action['happy']), False, (255, 255, 255))
        screen.blit(smile_text, (300, 15))
        health_text = pixel_font.render(str(action['health']), False, (255, 255, 255))
        screen.blit(health_text, (70, 75))
        info_health.blit_btn()

        tamagotchiAnimation(330, 340)

        btn_statistic.blit_btn()
        statistics = statisticsClass.Statistics(400, 250, 750, 450, abs_path('images/sprites/panel_brown.png'),
                                                str(action['logiki']) + ' Lg', 'Name: Tamagotchi', f'Days: {daysCount}')
        btn_satiety.blit_btn()
        btn_toilet.blit_btn()
        btn_play.blit_btn()
        btn_health.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endGame = True
                pygame.quit()
            if event.type == daysEvent:
                isSleep = True
            if not isSleep:
                if btn_statistic.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    statisticsClass.clicked_statistics = True
                    button_sound.play()
                if btn_satiety.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    foodClass.clicked_feed = True
                    button_sound.play()
                if action['logiki'] >= 0:
                    food.pressed(pos_x, pos_y, event)
                if btn_toilet.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    clearAfter()
                if btn_play.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    game_time = time.time()
                    playClass.clicked_play = True
                    button_sound.play()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(abs_path('sounds/game.ogg'))
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
                if event.type == pygame.USEREVENT:
                    if playClass.clicked_play:
                        spawn_coin(coins)
                if btn_health.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    medicine()
            if statistics.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                statisticsClass.clicked_statistics = False
                button_sound.play()
            if food.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                foodClass.clicked_feed = False
                button_sound.play()
            if play.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                playClass.clicked_play = False
                playClass.scoreCount = 0
                playClass.timeCount = 60
                playClass.seconds = 1
                button_sound.play()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(abs_path('sounds/backgroundMusic.ogg'))
                pygame.mixer.music.play(loops=-1)

        btn_statistic.hover(pos_x, pos_y)
        btn_satiety.hover(pos_x, pos_y)
        btn_toilet.hover(pos_x, pos_y)
        btn_play.hover(pos_x, pos_y)
        btn_health.hover(pos_x, pos_y)

        if isSleep:
            screen.blit(night_image, (735, 70))
            screen.blit(sleep_image, (430, 350))
            if night_timer > 700:
                isSleep = False
                night_timer = 0
                daysCount += 1
            night_timer += 1

        if cantClear:
            text = pixel_font.render('Not now...', True, (255, 255, 255))
            screen.blit(text, (230, 400))
            if text_timer > 75:
                cantClear = False
                text_timer = 0
            text_timer += 1

        if cantHelp:
            text = pixel_font.render('Not now...', True, (255, 255, 255))
            screen.blit(text, (660, 400))
            if text_timer > 75:
                cantHelp = False
                text_timer = 0
            text_timer += 1

        if statisticsClass.clicked_statistics:
            statistics.blit_statistics()
        if foodClass.clicked_feed:
            food.blit_food_menu()
            food.hover(pos_x, pos_y)
        if playClass.clicked_play:
            play.blit_play()
            basket.blit_basket()
            play.check_time(game_time)
            coins.draw(screen)
            coins.update(screen_height)
            if pygame.sprite.spritecollide(basket, coins, True):
                playClass.scoreCount += 1

        keys = pygame.key.get_pressed()
        play.control(keys)
        basket.control(keys)

        gameOver()

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        scoreTick()
        clock.tick(FPS)
        pygame.display.update()


def menu():
    global endMenu, animCount, start_time
    pygame.mixer.music.load(abs_path('sounds/menu.ogg'))
    pygame.mixer.music.play(loops=-1)
    while not endMenu:
        if animCount + 1 >= len(background_menu) * 9:
            animCount = 0
            screen.blit(background_menu[0], (0, 0))
        else:
            screen.blit(background_menu[animCount // 9], (0, 0))
            animCount += 1

        logika_label.blit_btn()
        start_btn.blit_btn()
        rule_btn.blit_btn()
        exit_btn.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endMenu = True
                pygame.quit()
            if start_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                endMenu = True
                game()
            if rule_btn.rect.collidepoint(pos_x, pos_y) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                panelClass.clicked_help = True
            if help_menu.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                panelClass.clicked_help = False
            if exit_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                pygame.mouse.set_visible(True)
                endMenu = True
                pygame.quit()

        start_btn.hover(pos_x, pos_y)
        rule_btn.hover(pos_x, pos_y)
        exit_btn.hover(pos_x, pos_y)

        if panelClass.clicked_help:
            help_menu.blit_panel()

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        clock.tick(FPS)
        pygame.display.update()

menu()
