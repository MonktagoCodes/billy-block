from grid import Grid
from blocks import *
import random
import pygame
import pygame.locals

pygame.mixer.init()
tetris_effect = pygame.mixer.Sound('BPVD4625.wav')
oneline_cleared_effect = pygame.mixer.Sound('IVVL9831.wav')
twoline_cleared_effect = pygame.mixer.Sound('QWSF6023.wav')
gameover_effect = pygame.mixer.Sound('Screen recording 2026-01-26 8.26.53 PM.wav')
lock_effect = pygame.mixer.Sound('mixkit-soccer-ball-quick-kick-2108.wav')
rotate_effect = pygame.mixer.Sound('496187__jonastisell__light-body-thud-on-clothing.mp3')
new_high_score = pygame.mixer.Sound('mixkit-bonus-earned-in-video-game-2058.wav')

lock_effect.set_volume(1)
rotate_effect.set_volume(1)
twoline_cleared_effect.set_volume(0.15)
tetris_effect.set_volume(0.3)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.highscore = self.load_highscore()
        self.lines_cleared = 0
        self.level = 1

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_highscore(self):
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))
        except Exception:
            pass

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
            twoline_cleared_effect.play()
        elif lines_cleared == 2:
            self.score += 300
            twoline_cleared_effect.play()
        elif lines_cleared == 3:
            self.score += 500
            twoline_cleared_effect.play()
        elif lines_cleared == 4:
            self.score += 1000
            tetris_effect.play()
        self.score += move_down_points
        self.lines_cleared += lines_cleared
        self.level = 1 + self.lines_cleared // 10
        if self.score > self.highscore:
            self.highscore = self.score
            new_high_score.play()
            self.save_highscore()

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            # Play lock sound immediately when block lands (natural or soft drop)
            if not hasattr(self, '_lock_sound_played') or not self._lock_sound_played:
                lock_effect.play()
                self._lock_sound_played = True
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True
        # Reset lock sound flag for next block
        self._lock_sound_played = False
            
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.highscore = self.load_highscore()
        self.lines_cleared = 0
        self.level = 1

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        rotate_effect.play()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        # Draw next block centered in the preview area
        self.next_block.draw(screen, 270, 270)