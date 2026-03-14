def draw_vertical_gradient(surface, rect, color1, color2):
    """Draw a vertical gradient from color1 (top) to color2 (bottom) in the given rect on surface."""
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w - 1, y + i))
import pygame
import sys
from game import Game
from block import *
from colors import Colors
import time
import asyncio

pygame.init()

# 500 620

BASE_W, BASE_H = 500, 725
virtual_surface = pygame.Surface((BASE_W, BASE_H))

screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Billy Blocks")


title_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 28)
large_title_font = pygame.font.Font(None, 45)
score_suface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
highscore_surface = title_font.render("High Score", True, Colors.white)
level_surface = small_font.render("Level", True, Colors.white)
game_title_surface = large_title_font.render("Billy Blocks Definitely Not Generic ;)", True, Colors.white)


score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
highscore_rect = pygame.Rect(320, 470, 170, 60)

# Add a small level box under high score (move lower)
level_rect = pygame.Rect(355, 570, 90, 35)

pygame.mixer.init()

try:
    gameover_effect = pygame.mixer.Sound('Screen recording 2026-01-26 8.26.53 PM.wav')
    move_effect = pygame.mixer.Sound('804721__designerschoice__beep-blue-snowball-microphone_high-pitched_nicholas-judy_tdc.wav')
    thud_effect = pygame.mixer.Sound('496187__jonastisell__light-body-thud-on-clothing.mp3')
    new_high_score = pygame.mixer.Sound('mixkit-bonus-earned-in-video-game-2058.wav')
    music1 = pygame.mixer.Sound('DFHV4665.wav')

except:
    print("Sound files not found, continuing without sound.")

clock = pygame.time.Clock()
game = Game()


def get_drop_interval(level):
    # Make level 1 much slower and make speed jumps bigger per level
    # Level 1: 500ms, Level 2: 350ms, Level 3: 200ms, Level 4+: 50ms
    return max(50, 500 - (level - 1) * 150)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, get_drop_interval(1))

music1.set_volume(0.25)
music1.play(-1)

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if game.game_over == True:
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    # Start soft drop: set fast timer
                    pygame.time.set_timer(GAME_UPDATE, 30)
                if event.key == pygame.K_UP and game.game_over == False:
                    game.rotate()
                    pygame.time.set_timer(GAME_UPDATE, 250)

            if event.type == GAME_UPDATE and game.game_over == False:
                game.move_down()
                # If soft drop is active, keep fast speed; else, update to normal interval for level
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    pygame.time.set_timer(GAME_UPDATE, 30)
                else:
                    # Always restore to correct level speed
                    pygame.time.set_timer(GAME_UPDATE, get_drop_interval(game.level))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and game.game_over == False:
                    # Always restore normal drop speed for current level after soft drop
                    pygame.time.set_timer(GAME_UPDATE, get_drop_interval(game.level))


        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        highscore_value_surface = title_font.render(str(game.highscore), True, Colors.white)
        level_value_surface = small_font.render(str(game.level), True, Colors.white)


        virtual_surface.fill(Colors.dark_blue)
        virtual_surface.blit(score_suface, (365, 20))
        virtual_surface.blit(game_title_surface, (5, 655))
        virtual_surface.blit(next_surface, (375, 180))
        highscore_label_rect = highscore_surface.get_rect(centerx=highscore_rect.centerx, centery=highscore_rect.top - 25)
        virtual_surface.blit(highscore_surface, highscore_label_rect)
        # Level label above level box (move label higher)
        level_label_rect = level_surface.get_rect(centerx=level_rect.centerx, centery=level_rect.top - 20)
        virtual_surface.blit(level_surface, level_label_rect)

        if game.game_over == True:
            virtual_surface.blit(game_over_surface, (320, 145))


        # Draw UI rectangles with gradient
        draw_vertical_gradient(virtual_surface, score_rect, Colors.light_blue, Colors.dark_blue)
        pygame.draw.rect(virtual_surface, Colors.white, score_rect, 2, 10)
        virtual_surface.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

        draw_vertical_gradient(virtual_surface, next_rect, Colors.light_blue, Colors.dark_blue)
        pygame.draw.rect(virtual_surface, Colors.white, next_rect, 2, 10)
        game.draw(virtual_surface)

        draw_vertical_gradient(virtual_surface, highscore_rect, Colors.light_blue, Colors.dark_blue)
        pygame.draw.rect(virtual_surface, Colors.white, highscore_rect, 2, 10)
        virtual_surface.blit(highscore_value_surface, highscore_value_surface.get_rect(centerx=highscore_rect.centerx, centery=highscore_rect.centery))

        # Draw level box and value
        draw_vertical_gradient(virtual_surface, level_rect, Colors.light_blue, Colors.dark_blue)
        pygame.draw.rect(virtual_surface, Colors.white, level_rect, 2, 8)

        virtual_surface.blit(level_value_surface, level_value_surface.get_rect(centerx=level_rect.centerx, centery=level_rect.centery))

        current_window_size = screen.get_size()
        scaled_surface = pygame.transform.scale(virtual_surface, current_window_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
