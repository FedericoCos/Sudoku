import pygame as pg
from pygame.locals import *
import sys
from copy import deepcopy
import time

# global variables
WIDTH = 600
HEIGHT = 600
FPS = 60
GRID_SIZE = 64
OFFSET_X = 12
OFFSET_Y = 12
FONT_SIZE = 32
UPDATE = 0.005

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Sudoku:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.surface = pg.display.get_surface()
    
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        
        self.mouse_pos = [0, 0]
        self.current_cell = [0, 0]
        self.cell_to_write = [-1, -1]
        
        self.number_font = pg.font.SysFont( None, FONT_SIZE )
        
        self.copy_of_grid = deepcopy(self.grid)
        self.solved = False
        
        
    
    def run(self):
        while True:
            self.clock.tick(FPS)
            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.cell_to_write[0], self.cell_to_write[1] = self.current_cell[0], self.current_cell[1]
                
                if event.type == pg.KEYDOWN:
                    if not self.solved:
                        if event.key == pg.K_1:
                            self.save_number(1)
                        if event.key == pg.K_2:
                            self.save_number(2)
                        if event.key == pg.K_3:
                            self.save_number(3)
                        if event.key == pg.K_4:
                            self.save_number(4)
                        if event.key == pg.K_5:
                            self.save_number(5)
                        if event.key == pg.K_6:
                            self.save_number(6)
                        if event.key == pg.K_7:
                            self.save_number(7)
                        if event.key == pg.K_8:
                            self.save_number(8)
                        if event.key == pg.K_9:
                            self.save_number(9)
                        if event.key == pg.K_BACKSPACE:
                            self.save_number(0)
                        
                    if event.key == pg.K_SPACE:
                        self.solved = True
                        self.backtracking()

            
            
            self.draw()
            
    def draw_grid(self):
        
        for i in range(10):
            pg.draw.line(self.surface, GREEN if i % 3 == 0 else WHITE, (OFFSET_X + i * GRID_SIZE, OFFSET_Y), (OFFSET_X + i * GRID_SIZE, OFFSET_Y + 9 * GRID_SIZE), 1)
            pg.draw.line(self.surface, GREEN if i % 3 == 0 else WHITE, (OFFSET_X, OFFSET_Y + i * GRID_SIZE), (OFFSET_X + GRID_SIZE * 9, OFFSET_Y + i * GRID_SIZE), 1)
            
    def mouse_overlay(self, mouse_pos):
        if OFFSET_X <= mouse_pos[0] < WIDTH - OFFSET_X and OFFSET_Y <= mouse_pos[1] < HEIGHT - OFFSET_Y:
            mouse_pos[0] -= OFFSET_X
            mouse_pos[1] -= OFFSET_Y
            
            self.current_cell[0], self.current_cell[1] = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
            rect = Rect(OFFSET_X + self.current_cell[0] * GRID_SIZE + 1, OFFSET_Y + self.current_cell[1] * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pg.draw.rect(self.surface, GREY, rect)
        
        if self.cell_to_write[0] != -1 and self.cell_to_write[1] != -1:
            rect = Rect(OFFSET_X + self.cell_to_write[0] * GRID_SIZE + 1, OFFSET_Y + self.cell_to_write[1] * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pg.draw.rect(self.surface, GREY, rect)
    
    
    def save_number(self, num):
        self.grid[self.cell_to_write[0]][self.cell_to_write[1]] = num
        self.cell_to_write = [-1, -1]
        
    def draw_fixed_numbers(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    number_image = self.number_font.render(str(self.grid[i][j]), BLACK, RED)
                    self.surface.blit(number_image, (OFFSET_X + i * GRID_SIZE + GRID_SIZE / 2 - FONT_SIZE // 4,
                                                     OFFSET_Y + j * GRID_SIZE + GRID_SIZE / 2 - FONT_SIZE // 4))
                elif self.copy_of_grid[i][j] != 0:
                    number_image = self.number_font.render(str(self.copy_of_grid[i][j]), BLACK, WHITE)
                    self.surface.blit(number_image, (OFFSET_X + i * GRID_SIZE + GRID_SIZE / 2 - FONT_SIZE // 4,
                                                     OFFSET_Y + j * GRID_SIZE + GRID_SIZE / 2 - FONT_SIZE // 4))
                    
    def backtracking(self):
        self.cell_to_write = [-1, -1]
        self.copy_of_grid = deepcopy(self.grid)
        return self.recursive_solver(0, 0)
        
        
    
    def recursive_solver(self, i, j):
        if i == 9:
            return True
        
        if(self.grid[i][j] == 0):
            for num in range(9):
                self.copy_of_grid[i][j] = num + 1
                if self.valid():
                    self.draw()
                    time.sleep(UPDATE)
                    new_j = (j + 1) % 9
                    new_i = i + (j + 1) // 9
                    
                    if self.recursive_solver(new_i, new_j):
                        return True
                
                self.copy_of_grid[i][j] = 0
        else:
            new_j = (j + 1) % 9
            new_i = i + (j + 1) // 9
            
            if self.recursive_solver(new_i, new_j):
                return True
        
        return False
            
    
    def valid(self):
        for i in range(9):
            if not self.valid_col(i) or not self.valid_row(i):
                return False
        
        for i in range(3):
            for j in range(3):
                if not self.valid_box(i * 3, j * 3):
                    return False
        
        return True
    
    def valid_col(self, col):
        values = {i: 0 for i in range(1, 10)}
        
        for i in range(9):
            if self.copy_of_grid[col][i] != 0:
                values[self.copy_of_grid[col][i]] += 1
                if values[self.copy_of_grid[col][i]] > 1:
                    return False
        
        return True
        
    
    def valid_row(self, row):
        values = {i: 0 for i in range(1, 10)}
        
        for i in range(9):
            if self.copy_of_grid[i][row] != 0:
                values[self.copy_of_grid[i][row]] += 1
                if values[self.copy_of_grid[i][row]] > 1:
                    return False
        
        return True
    
    def valid_box(self, row,col):
        values = {i: 0 for i in range(1, 10)}
        
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                if self.copy_of_grid[i][j] != 0:
                    values[self.copy_of_grid[i][j]] += 1
                    if values[self.copy_of_grid[i][j]] > 1:
                        return False
                    
        return True
    
    
    def draw(self):
        self.screen.fill(BLACK)
            
        self.draw_grid()
        
        if not self.solved:
            mouse_pos = pg.mouse.get_pos()
            self.mouse_pos[0] = mouse_pos[0]
            self.mouse_pos[1] = mouse_pos[1]
            self.mouse_overlay(self.mouse_pos)
        
        self.draw_fixed_numbers()
        
        
        pg.display.flip()
              
                
            
            


sudoku = Sudoku()
sudoku.run()