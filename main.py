import random

import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run_1 = pygame.image.load('Graphics/Player_run_1.png').convert_alpha()
        player_run_2 = pygame.image.load('Graphics/Player_run_2.png').convert_alpha()
        player_run_3 = pygame.image.load('Graphics/Player_run_3.png').convert_alpha()
        player_run_4 = pygame.image.load('Graphics/Player_run_4.png').convert_alpha()
        player_run_5 = pygame.image.load('Graphics/Player_run_5.png').convert_alpha()
        player_run_6 = pygame.image.load('Graphics/Player_run_6.png').convert_alpha()
        player_run_7 = pygame.image.load('Graphics/Player_run_7.png').convert_alpha()
        player_run_8 = pygame.image.load('Graphics/Player_run_8.png').convert_alpha()
        player_run_9 = pygame.image.load('Graphics/Player_run_9.png').convert_alpha()
        self.player_run = [
            player_run_1,
            player_run_2,
            player_run_3,
            player_run_4,
            player_run_5,
            player_run_6,
            player_run_7,
            player_run_8,
            player_run_9,
        ]
        self.animation_index = 0
        self.player_jump = pygame.image.load('Graphics/Player_jump.png').convert_alpha()

        self.image = player_run_1
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.rect.width = self.image.get_width() // 2
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            if display_score() > 10:
                self.gravity = -15

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.animation_index += 0.3
            if self.animation_index >= len(self.player_run):
                self.animation_index = 0
            self.image = self.player_run[int(self.animation_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'bird':
            bird_frame_1 = pygame.image.load('Graphics/Enemy_bird_1.png').convert_alpha()
            bird_frame_2 = pygame.image.load('Graphics/Enemy_bird_2.png').convert_alpha()
            self.frames = [bird_frame_1, bird_frame_2]
            y_pos = 160
        else:
            boulder_frame_1 = pygame.image.load('Graphics/Enemy_boulder_1.png').convert_alpha()
            boulder_frame_2 = pygame.image.load('Graphics/Enemy_boulder_2.png').convert_alpha()
            self.frames = [boulder_frame_1, boulder_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -200:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= speed
        self.destroy()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coin_frame_1 = image_scaling('Graphics/Coin_1.png', 45, 45)
        coin_frame_2 = image_scaling('Graphics/Coin_2.png', 45, 45)
        coin_frame_3 = image_scaling('Graphics/Coin_3.png', 45, 45)
        coin_frame_4 = image_scaling('Graphics/Coin_2.png', 45, 45)
        self.coin_frame = [
            coin_frame_1,
            coin_frame_2,
            coin_frame_3,
            coin_frame_4
        ]

        self.animation_index = 0
        self.image = coin_frame_1
        y_pos = [280, 280, 160]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1700), choice(y_pos)))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.coin_frame):
            self.animation_index = 0
        self.image = self.coin_frame[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -200:
            self.kill()
            return True
        if not player_collisions(coin_group, False):
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
    score_surf = font.render(f'{current_time}', True, 'black')
    score_rect = score_surf.get_rect(midleft = (10, 20))
    screen.blit(score_surf, score_rect)
    return current_time

def player_collisions(group, empty):
    if pygame.sprite.spritecollide(player_group.sprite, group, False):
        if empty:
            group.empty()
        return False
    else:
        return True

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

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
pygame.display.set_icon(pygame.image.load('Graphics/Logo.png'))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/MP16REG.ttf', 30)
coin_spawn_random = 0
game_active = True
start_time = 0
speed = 10
money = 0


# Groups
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

obstacle_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()

# Background colour
background_surf = image_scaling('Graphics/Background.png', 800, 400)

# Ground
ground_surf = pygame.image.load('Graphics/Ground.png').convert()
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
obstacle_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_spawn_timer, 700)

bird_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bird_animation_timer, 100)

boulder_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(boulder_animation_timer, 100)

coin_spawn_timer = pygame.USEREVENT + 4
pygame.time.set_timer(coin_spawn_timer, 1500)

obstacle_speed = pygame.USEREVENT + 5
pygame.time.set_timer(obstacle_speed, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_spawn_timer:
                obstacle_group.add(Obstacle(choice(['bird', 'boulder', 'boulder'])))

            if event.type == coin_spawn_timer:
                coin_group.add(Coin())

            if event.type == obstacle_speed:
                speed += 0.01 # default: 0.01

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_time = pygame.time.get_ticks()
                    game_active = True

    if game_active:
        # Background
        screen.blit(background_surf, (0, 0))
        city3_x1, city3_x2 = scroll_background(city3_x1, city3_x2, city3_surf, 0, city3_img_width, 3000)
        city2_x1, city2_x2 = scroll_background(city2_x1, city2_x2, city2_surf, 0, city2_img_width, 800)
        city_x1, city_x2 = scroll_background(city_x1, city_x2, city_surf, 0, city_img_width, 100)
        ground_x1, ground_x2 = scroll_background(ground_x1, ground_x2, ground_surf, 300, ground_img_width, 1.5)

        # Score and money display
        score = display_score()
        money_message = font.render(f'${int(money)}', True, 'black')
        money_message_rect= money_message.get_rect(midleft = (10, 50))
        screen.blit(money_message, money_message_rect)
        # Player
        player_group.update()
        player_group.draw(screen)
        obstacle_group.draw(screen)
        obstacle_group.update()
        coin_group.draw(screen)
        coin_group.update()
        game_active = player_collisions(obstacle_group, True)

    else:
        speed = 10
        score_surf2 = font.render('PRESS SPACE BAR TO RESTART', False, 'white')
        score_rect2 = score_surf2.get_rect(center = (400, 200))
        score_message = font.render(f'score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 50))
        screen.fill('black')
        screen.blit(score_message, score_message_rect)
        screen.blit(score_surf2, score_rect2)

    pygame.display.update()
    clock.tick(60)
