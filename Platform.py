import math
import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 660

background_img = pygame.image.load("background.png")
player_img = pygame.image.load("player.png")
platform_img = pygame.image.load("platform.png")

player_img = pygame.transform.scale(player_img, (40, 60))
platform_img = pygame.transform.scale(platform_img, (150, 30))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BROWN = (189,69,19)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 48)

player_width = 40
player_height = 60
player_x = random.randint(100, SCREEN_WIDTH - player_width)
player_y = SCREEN_HEIGHT - 20 - player_height
player_speed = 5
player_jump_speed = 15
gravity = 0.8

player_velocity_y = 0
is_jumping = False

def generate_platforms():
    platforms = [pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)] 
    while len(platforms) < math.ceil(SCREEN_HEIGHT/player_height):
        x = random.randint(0, SCREEN_WIDTH - 200)
        y = random.randint(150, SCREEN_HEIGHT - 100)  
        new_platform = pygame.Rect(x, y, 150, 20)
        if all(not new_platform.colliderect(p) for p in platforms):  
            platforms.append(new_platform)
    return sorted(platforms, key=lambda p: p.top, reverse=True)  

platforms = generate_platforms()

message_displayed = False

def draw_message_bg(text, color, y_offset=0):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(message, text_rect)

def draw_message(text, color, y_offset=0):
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(message, text_rect)

def main():
    global player_x, player_y, player_velocity_y, is_jumping, platforms, message_displayed

    running = True
    while running:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if message_displayed and event.key == pygame.K_r:
                    player_x, player_y = 100, SCREEN_HEIGHT - 20 - player_height  
                    player_velocity_y = 0
                    is_jumping = False
                    message_displayed = False
                    platforms = generate_platforms() 
                     
        keys = pygame.key.get_pressed()
        if not message_displayed:
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
            if keys[pygame.K_SPACE] and not is_jumping:
                player_velocity_y = -player_jump_speed
                is_jumping = True

        if not message_displayed:
            player_velocity_y += gravity
            player_y += player_velocity_y

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for platform in platforms:
            if player_rect.colliderect(platform) and player_velocity_y > 0:
                player_y = platform.top - player_height
                player_velocity_y = 0
                is_jumping = False
                break

        topmost_platform = platforms[-1]
        if player_rect.colliderect(topmost_platform) and not message_displayed:
            message_displayed = True

        if player_y > SCREEN_HEIGHT:
            player_x, player_y = 100, SCREEN_HEIGHT - 20 - player_height
            player_velocity_y = 0
            is_jumping = False
            platforms = generate_platforms()

        pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)) 

        for platform in platforms:
            screen.blit(platform_img, (platform.x, platform.y))

        if not message_displayed:
            screen.blit(player_img, (player_x, player_y))
        
        if message_displayed:
            draw_message_bg("Press 'R' to Reset", YELLOW, 50)
            draw_message("Congratulations! You reached the top!", RED, 0)

        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
