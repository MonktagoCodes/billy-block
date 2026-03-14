import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for  row  in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()


    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0


    def draw(self, screen):
        from block import Block  # avoid circular import at top
        dummy_block = Block(1)
        # Draw grid lines first (beneath blocks)
        grid_left = 11
        grid_top = 11
        grid_color = (120, 120, 140)  # lighter, neutral gray for grid lines
        for row in range(self.num_rows + 1):
            y = grid_top + row * self.cell_size
            pygame.draw.line(screen, grid_color, (grid_left, y), (grid_left + self.num_cols * self.cell_size, y), 1)
        for col in range(self.num_cols + 1):
            x = grid_left + col * self.cell_size
            pygame.draw.line(screen, grid_color, (x, grid_top), (x, grid_top + self.num_rows * self.cell_size), 1)
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_size = self.cell_size
                x = column * cell_size + 11
                y = row * cell_size + 11
                if cell_value == 0:
                    # Draw empty grid square as a lighter black (dark gray)
                    empty_color = (36, 36, 36)  # not too dark, but still black
                    pygame.draw.rect(screen, empty_color, (x + 1, y + 1, cell_size - 2, cell_size - 2))
                    # Draw border for empty cell for clarity
                    pygame.draw.rect(screen, (20, 20, 20), (x, y, cell_size, cell_size), 1)
                else:
                    # Draw locked block cell with gradient and border
                    base_color = self.colors[cell_value]
                    tile_rect = pygame.Rect(x + 1, y + 1, cell_size - 2, cell_size - 2)
                    light_color = tuple(min(255, int(c * 1.25 + 40)) for c in base_color)
                    dark_color = tuple(max(0, int(c * 0.65)) for c in base_color)
                    for i in range(tile_rect.height):
                        ratio = i / tile_rect.height
                        if ratio < 0.5:
                            blend = ratio * 2
                            r = int(light_color[0] * (1 - blend) + base_color[0] * blend)
                            g = int(light_color[1] * (1 - blend) + base_color[1] * blend)
                            b = int(light_color[2] * (1 - blend) + base_color[2] * blend)
                        else:
                            blend = (ratio - 0.5) * 2
                            r = int(base_color[0] * (1 - blend) + dark_color[0] * blend)
                            g = int(base_color[1] * (1 - blend) + dark_color[1] * blend)
                            b = int(base_color[2] * (1 - blend) + dark_color[2] * blend)
                        pygame.draw.line(screen, (r, g, b), (tile_rect.left, tile_rect.top + i), (tile_rect.right, tile_rect.top + i))
                    border_rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(screen, (20, 20, 20), border_rect, 1)