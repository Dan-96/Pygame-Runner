import random

import time

import pygame

from time import sleep

from sys import exit

from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_index = 0
        self.player_jump = pygame.image.load('Graphics/Player_jump.png').convert_alpha()
        self.player_slide = image_scaling('Graphics/Player_slide.png', 125, 55)
        self.image = import_frames('Player_run_', 10)[0]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.rect.width = self.image.get_width() // 2
        self.gravity = 0
        self.sliding_cooldown = False
        self.sliding_time = 0

    def player_input(self):
        if display_score() > 5:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.rect.bottom >= 300:
                self.gravity = -15

            if keys[pygame.K_DOWN] and self.rect.bottom == 300:
                if not self.sliding_cooldown:
                    self.image = self.player_slide
                    self.rect.y += 80
                    self.sliding_time = pygame.time.get_ticks()
                    self.sliding_cooldown = True

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.animation_index += speed / 50  # default: 50
            if self.animation_index >= len(import_frames('Player_run_', 10)):
                self.animation_index = 0

            self.image = import_frames('Player_run_', 10)[int(self.animation_index)]
            self.rect = self.image.get_rect(midbottom=(80, 300))
            self.rect.width = self.image.get_width() // 2


    def update(self):
        if self.sliding_cooldown:
            current_time = pygame.time.get_ticks()
            if current_time - self.sliding_time > 500:
                self.image = import_frames('Player_run_', 10)[0]
                self.rect = self.image.get_rect(midbottom=(80, 300))
                self.rect.width = self.image.get_width() // 2
                self.sliding_cooldown = False

        else:
            self.apply_gravity()
            self.animation_state()
            self.player_input()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'bird':
            self.frames = import_frames('Enemy_bird_', 3)
            self.y_pos = choice([160, 240])

        else:
            self.frames = import_frames('Enemy_boulder_', 3)
            self.y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.y_pos))
        self.rect.width = self.image.get_width() // 10
        self.rect.height = self.image.get_height() // 10

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -300:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= speed
        self.destroy()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_spin = import_frames('Coin_', 5, True, 40, 40)
        self.animation_index = 0
        self.image = self.coin_spin[0]
        y_pos = [280, 280, 160]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1700), choice(y_pos)))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.coin_spin):
            self.animation_index = 0

        self.image = self.coin_spin[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -200:
            self.kill()
            return True

        if player_collisions(coin_group, False):
            self.kill()
            global money
            money += 1
            return True

        else:
            return False

    def update(self):
        self.animation_state()
        self.rect.x -= speed / 1.5
        self.destroy()


def display_score():
    current_time = int(round((pygame.time.get_ticks() - start_time) / 100))
    score_surf = font.render(f'{current_time}m', False, 'black')
    score_rect = score_surf.get_rect(midleft = (10, 20))
    screen.blit(score_surf, score_rect)
    return current_time

def player_collisions(group, empty):
    if pygame.sprite.spritecollide(player_group.sprite, group, False):
        if empty:
            group.empty()

        return True

    else:
        return False

def scroll_background(bg_x, bg_x2, surface, height, img_width, scroll_speed):
    bg_x -= speed / scroll_speed
    bg_x2 -= speed / scroll_speed
    if bg_x < -img_width:
        bg_x = bg_x2 + img_width

    if bg_x2 < -img_width:
        bg_x2 = bg_x + img_width

    screen.blit(surface, (bg_x, height))
    screen.blit(surface, (bg_x2, height))
    return bg_x, bg_x2

def image_scaling(image, x, y):
    return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (x, y))

def menu_selection(y_pos, x_pos = 300):
    selection_surf = pygame.image.load('Graphics/Selection.png').convert_alpha()
    selection_rect = selection_surf.get_rect(topleft = (x_pos, y_pos))
    screen.blit(selection_surf, selection_rect)

def text_render(text, color, x, y, anchor = 'center'):
    if menu_position == y - 25:
        color = 'white'

    surf = font.render(text, False, color)
    rect = surf.get_rect()
    setattr(rect, anchor, (x, y))
    screen.blit(surf, rect)
    return surf

def import_frames(image, number_of_frames, scaling = False, x = None, y = None):
    img_list = []
    for i in range(1, number_of_frames):
        img_path = f'Graphics/{image}{i}.png'
        if scaling:
            img = image_scaling(img_path, x, y).convert_alpha()
        else:
            img = pygame.image.load(img_path).convert_alpha()
        img_list.append(img)

    return img_list

def timer(number, milliseconds):
    time = pygame.USEREVENT + number
    pygame.time.set_timer(time, milliseconds)
    return time

def blur(amount):
    overlay = pygame.Surface((800, 400))
    overlay.set_alpha(amount)
    # overlay.fill('black')
    screen.blit(overlay, (0, 0))

# Main
pygame.init()
WIDTH = 800
HEIGHT = 400
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Runner')
pygame.display.set_icon(pygame.image.load('Graphics/Logo.png'))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/MP16REG.ttf', 30)
credits_x, credits_y = 245, 12
random_speed_x = random.uniform(0.05, 0.2)
random_speed_y = random.uniform(0.05, 0.2)
credits_color = (randint(1, 255), randint(1, 255), randint(1, 255))
game_active = False
options_menu = False
credits_menu = False
menu_position = 125
start_time = 0
speed = 10
money = 0
score = 0
alpha = 0


# Groups
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

obstacle_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()

# Background
background_surf = image_scaling('Graphics/Background.png', 800, 400)

# Ground
ground_surf = pygame.image.load('Graphics/Ground.png').convert_alpha()
ground_img_width = ground_surf.get_width()
ground_x1 = 0
ground_x2 = ground_img_width

# Background city
city_surf = image_scaling('Graphics/City_background_1.png', 800, 400)
city_img_width = city_surf.get_width()
city_x1 = 0
city_x2 = city_img_width

city2_surf = image_scaling('Graphics/City_background_2.png', 800, 400)
city2_img_width = city2_surf.get_width()
city2_x1 = 0
city2_x2 = city2_img_width

city3_surf = image_scaling('Graphics/City_background_3.png', 800, 400)
city3_img_width = city3_surf.get_width()
city3_x1 = 0
city3_x2 = city3_img_width

# Timers
obstacle_spawn_timer = timer(1, 700)
bird_animation_timer = timer(2, 100)
boulder_animation_timer = timer(3, 100)
coin_spawn_timer = timer(4, 1500)
obstacle_speed = timer(5, 50)
credits_scroll_timer = timer(6, 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False

            if event.type == obstacle_spawn_timer:
                obstacle_group.add(Obstacle(choice(['bird', 'boulder', 'boulder'])))

            if event.type == coin_spawn_timer:
                if score > 100:
                    coin_group.add(Coin())

            if event.type == obstacle_speed:
                speed += 0.01 # default: 0.01
                if speed >= 20:
                    speed = 20
                print(round(speed, 2))

        elif options_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if menu_position == 175:
                        options_menu = False
                        menu_position = 125

                if event.key == pygame.K_ESCAPE:
                    options_menu = False
                    menu_position = 75

                if event.key == pygame.K_DOWN:
                    menu_position += 50
                    if menu_position >= 175:
                        menu_position = 175

                if event.key == pygame.K_UP:
                    menu_position -= 50
                    if menu_position <= 175:
                        menu_position = 175

        elif credits_menu:
            if event.type == pygame.KEYDOWN:
                credits_menu = False
                menu_position = 125

            credits_y += random_speed_y
            credits_x += random_speed_x
            if credits_y >= 385:
                random_speed_y = -random.uniform(0.05, 0.2)
                credits_y = 385
                credits_color = (randint(1, 255), randint(1, 255), randint(1, 255))

            elif credits_y <= 12:
                random_speed_y = random.uniform(0.05, 0.2)
                credits_y = 12
                credits_color = (randint(1, 255), randint(1, 255), randint(1, 255))

            if credits_x >= 560:
                random_speed_x = -random.uniform(0.05, 0.2)
                credits_x = 560
                credits_color = (randint(1, 255), randint(1, 255), randint(1, 255))

            elif credits_x <= 245:
                random_speed_x = random.uniform(0.05, 0.2)
                credits_x = 245
                credits_color = (randint(1, 255), randint(1, 255), randint(1, 255))


        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if menu_position == 125:
                        start_time = pygame.time.get_ticks()
                        game_active = True

                    if menu_position == 175:
                        options_menu = True
                        menu_position = 175

                    if menu_position == 225:
                        screen.fill('black')
                        credits_menu = True

                    if menu_position == 275:
                        pygame.quit()
                        exit()

                if event.key == pygame.K_DOWN:
                    menu_position += 50
                    if menu_position >= 275:
                        menu_position = 275

                if event.key == pygame.K_UP:
                    menu_position -= 50
                    if menu_position <= 125:
                        menu_position = 125


    if game_active:
        # Background
        screen.blit(background_surf, (0, 0))
        city3_x1, city3_x2 = scroll_background(city3_x1, city3_x2, city3_surf, 0, city3_img_width, 3000)
        city2_x1, city2_x2 = scroll_background(city2_x1, city2_x2, city2_surf, 0, city2_img_width, 800)
        city_x1, city_x2 = scroll_background(city_x1, city_x2, city_surf, 0, city_img_width, 100)
        ground_x1, ground_x2 = scroll_background(ground_x1, ground_x2, ground_surf, 300, ground_img_width, 1.5)

        # Score and money display
        score = display_score()
        text_render(f'${int(money)}', 'black', 10, 50, 'midleft')

        # Drawing
        obstacle_group.update()
        obstacle_group.draw(screen)
        coin_group.update()
        coin_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        game_active = not player_collisions(obstacle_group, True)

    elif options_menu:
        blur(30)
        text_render('BACK', 'gray60', 400, 200)
        menu_selection(menu_position)

    elif credits_menu:
        blur(99.99)
        text_render('Game developed by Daniel Michalczyk', credits_color, credits_x, credits_y)

    else:
        speed = 10
        coin_group.empty()
        text_render('START', 'gray60', 400, 150)
        text_render('OPTIONS', 'gray60', 400, 200)
        text_render('CREDITS', 'gray60', 400, 250)
        text_render('QUIT', 'gray60', 400, 300)
        text_render(f'{score} meters', 'white', 400, 20)
        text_render(f'${money}', 'white', 400, 50)

        # Screen update
        menu_selection(menu_position)
        blur(30)

    pygame.display.update()
    clock.tick(FPS)