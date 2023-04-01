import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Player_run_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 300))


def display_score():
    current_time = int(round((pygame.time.get_ticks() - start_time) / 100))
    score_surf = font.render(f'{current_time}', True, 'black')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.left -= 15
            if obstacle_rect.bottom == 300:
                screen.blit(boulder_surf, obstacle_rect)
            else:
                screen.blit(bird_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.left > -200]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animations():
    global player_surf, player_index
    if player_rect.bottom < 300:
        # Jumping animation
        player_surf = player_jump
    else:
        # Walking animation
        player_index += 0.3
        if player_index >= len(player_run):
            player_index = 0
        player_surf = player_run[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
pygame.display.set_icon(pygame.image.load('Graphics/Logo.png'))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/MP16REG.ttf', 50)
game_active = True
start_time = 0
player = pygame.sprite.GroupSingle()
player.add(Player())

# Background and ground
background_surf = pygame.transform.scale((pygame.image.load('Graphics/Background.png').convert()), (800, 400))
ground_surf = pygame.image.load('Graphics/Ground.png').convert()
ground_rect = ground_surf.get_rect()

# Boulder obstacle
boulder_frame_1 = pygame.image.load('Graphics/Enemy_boulder_1.png').convert_alpha()
boulder_frame_2 = pygame.image.load('Graphics/Enemy_boulder_2.png').convert_alpha()
boulder_frames = [boulder_frame_1, boulder_frame_2]
boulder_frame_index = 0
boulder_surf = boulder_frames[int(boulder_frame_index)]

# Bird obstacle
bird_frame_1 = pygame.image.load('Graphics/Enemy_bird_1.png').convert_alpha()
bird_frame_2 = pygame.image.load('Graphics/Enemy_bird_2.png').convert_alpha()
bird_frames = [bird_frame_1, bird_frame_2]
bird_frame_index = 0
bird_surf = bird_frames[int(bird_frame_index)]

# Obstacle list
obstacle_rect_list = []

# Player walk
player_run_1 = pygame.image.load('Graphics/Player_run_1.png').convert_alpha()
player_run_2 = pygame.image.load('Graphics/Player_run_2.png').convert_alpha()
player_run_3 = pygame.image.load('Graphics/Player_run_3.png').convert_alpha()
player_run_4 = pygame.image.load('Graphics/Player_run_4.png').convert_alpha()
player_run_5 = pygame.image.load('Graphics/Player_run_5.png').convert_alpha()
player_run_6 = pygame.image.load('Graphics/Player_run_6.png').convert_alpha()
player_run_7 = pygame.image.load('Graphics/Player_run_7.png').convert_alpha()
player_run_8 = pygame.image.load('Graphics/Player_run_8.png').convert_alpha()
player_run_9 = pygame.image.load('Graphics/Player_run_9.png').convert_alpha()

player_run = [
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

# Player jump
player_jump = pygame.image.load('Graphics/Player_jump.png').convert_alpha()

player_index = 0

player_surf = player_run[player_index]
player_rect = player_surf.get_rect(midbottom = (50, 300))
player_gravity = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 700)

bird_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bird_animation_timer, 100)

boulder_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(boulder_animation_timer, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(boulder_frame_1.get_rect(midbottom = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(bird_frame_1.get_rect(midbottom=(randint(900, 1100), 150)))

            if event.type == boulder_animation_timer:
                if boulder_frame_index == 0:
                    boulder_frame_index = 1
                else:
                    boulder_frame_index = 0
                boulder_surf = boulder_frames[boulder_frame_index]

            if event.type == bird_animation_timer:
                if bird_frame_index == 0:
                    bird_frame_index = 1
                else:
                    bird_frame_index = 0
                bird_surf = bird_frames[bird_frame_index]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -16

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom >= 300:
                        player_gravity = -16

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_time = pygame.time.get_ticks()
                    game_active = True

    if game_active:
        screen.blit(background_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animations()
        player.draw(screen)
        screen.blit(player_surf, player_rect)
        player_rect.top += player_gravity

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions with enemy
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (50, 300)
        player_gravity = 0
        score_surf2 = font.render('PRESS SPACE BAR TO RESTART', False, 'white')
        score_rect2 = score_surf2.get_rect(center=(400, 200))
        score_message = font.render(f'score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 50))
        screen.fill('black')
        screen.blit(score_message, score_message_rect)
        screen.blit(score_surf2, score_rect2)

    pygame.display.update()
    clock.tick(60)
