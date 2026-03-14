from colors import Colors
import pygame
from position import Position
import random

class Block:
    def __init__(self, id):
        self.colors = Colors.get_cell_colors()
        self.id = random.randint(1, len(self.colors) -1)
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offeset_y):
        tiles = self.get_cell_positions()
        base_color = self.colors[self.id]
        # Smoother vertical gradient: blend from lighter to base to darker
        for tile in tiles:
            # Shrink the gradient area to leave a 1px gap between blocks
            tile_rect = pygame.Rect(
                offset_x + tile.column * self.cell_size + 1,
                offeset_y + tile.row * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2)
            light_color = tuple(min(255, int(c * 1.25 + 40)) for c in base_color)
            dark_color = tuple(max(0, int(c * 0.65)) for c in base_color)
            for i in range(tile_rect.height):
                ratio = i / tile_rect.height
                if ratio < 0.5:
                    # Blend from light to base
                    blend = ratio * 2
                    r = int(light_color[0] * (1 - blend) + base_color[0] * blend)
                    g = int(light_color[1] * (1 - blend) + base_color[1] * blend)
                    b = int(light_color[2] * (1 - blend) + base_color[2] * blend)
                else:
                    # Blend from base to dark
                    blend = (ratio - 0.5) * 2
                    r = int(base_color[0] * (1 - blend) + dark_color[0] * blend)
                    g = int(base_color[1] * (1 - blend) + dark_color[1] * blend)
                    b = int(base_color[2] * (1 - blend) + dark_color[2] * blend)
                pygame.draw.line(screen, (r, g, b), (tile_rect.left, tile_rect.top + i), (tile_rect.right, tile_rect.top + i))
            # Draw a dark border for extra clarity
            border_rect = pygame.Rect(
                offset_x + tile.column * self.cell_size,
                offeset_y + tile.row * self.cell_size,
                self.cell_size,
                self.cell_size)
            pygame.draw.rect(screen, (20, 20, 20), border_rect, 1)