import pygame
import numpy as np

width = 1280
height = 720
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font(None, 36) 
class Grid:
  def __init__(self,rows=9, columns=16,numberofmines=20):
    self.rows = rows
    self.columns = columns
    self.numberofmines = numberofmines
    self.grid = self.setupGrid()
  
  def setupGrid(self):
    grid = np.zeros((rows, columns), dtype=int)
    minepositions = np.random.choice(grid.size, self.numberofmines,replace=False)
    np.put(self.grid, minepositions, 1)
    
  def checkForMines(self,row,col):
    if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
        return 0

    # Define the boundaries for checking neighboring cells.
    row_start = max(0, row - 1)
    row_end = min(self.rows - 1, row + 1)
    col_start = max(0, col - 1)
    col_end = min(self.columns - 1, col + 1)

    # Count the number of mines in the neighboring cells.
    mine_count = np.sum(self.grid[row_start:row_end + 1, col_start:col_end + 1])

    # Exclude the cell itself from the count (if it's a mine).
    if self.grid[row, col] == 1:
        mine_count -= 1

    return mine_count
  
  def displayGrid(self):
    print(self.grid)
    for r in range(0,self.rows):
      for c in range(0,self.columns):
        if self.grid[r][c] == 1:
          print("X",end="")
        else:
          print(self.checkForMines(r,c),end="")
      print("")
  
  def drawGrid(self, surface):
    gridWidth = width/grid.columns
    gridHeight = height/grid.rows
    for y in range(grid.rows):
        for x in range(grid.columns):
            rect = pygame.Rect(x * gridHeight, y * gridWidth, gridWidth, gridHeight)
            if self.grid[y][x] == 1:
                pygame.draw.rect(surface, (255,255,255), rect)
            else:
                pygame.draw.rect(surface, (0,0,0), rect)
                mine_count = self.checkForMines(y, x)
                if mine_count > 0:
                    text_surface = font.render(str(mine_count), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=rect.center)
                    surface.blit(text_surface, text_rect)
            pygame.draw.rect(surface, (50, 50, 50), rect, 1)  
    print(x,y)
    
grid = Grid()
grid.setupGrid()
grid.displayGrid()
grid.drawGrid(screen)
pygame.display.update()
loop=True
while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      loop=False
  
  pygame.display.update()
  
pygame.quit()