import pygame
from sys import exit


def display_score():
    current_time = int(round((pygame.time.get_ticks() - start_time) / 100))
    score_surf = font.render(f'{current_time}', True, 'black')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
pygame.display.set_icon(pygame.image.load('Graphics/Logo.png'))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/MP16REG.ttf', 50)
game_active = True
start_time = 0

background_surf = pygame.image.load('Graphics/Background.png').convert()
ground_surf = pygame.image.load('Graphics/Ground.png').convert()
ground_rect = ground_surf.get_rect()


# score_surf = font.render('0', False, 'black')
# score_rect = score_surf.get_rect(center = (400, 50))

enemy_surf = pygame.image.load('Graphics/Enemy_golf.png').convert_alpha()
enemy_rect = enemy_surf.get_rect(topleft = (800, 245))

player_surf = pygame.image.load('Graphics/Player_Idle.png')
player_rect = player_surf.get_rect(midbottom = (50, 300))
player_gravity = 0

mouse_pos = pygame.mouse.get_pos()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom >= 300:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_time = pygame.time.get_ticks()
                    game_active = True

    if game_active:
        screen.blit(background_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()
        enemy_rect.left -= 15
        if enemy_rect.left < -200:
            enemy_rect.left = 800
        screen.blit(enemy_surf, enemy_rect)
        # player
        player_gravity += 1
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        player_rect.top += player_gravity
        # collisions with enemy
        if player_rect.colliderect(enemy_rect):
            if player_rect.collidepoint(enemy_rect.topleft) or \
                    player_rect.collidepoint(enemy_rect.topright) or \
                    player_rect.collidepoint(enemy_rect.bottomleft) or \
                    player_rect.collidepoint(enemy_rect.bottomright):
                enemy_rect.left = 800
                game_active = False

    else:
        score_surf2 = font.render('PRESS SPACE BAR TO RESTART', False, 'white')
        score_rect2 = score_surf2.get_rect(center=(400, 200))
        score_message = font.render(f'score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 50))
        screen.fill('black')
        screen.blit(score_message, score_message_rect)
        screen.blit(score_surf2, score_rect2)

    pygame.display.update()
    clock.tick(60)