import pygame
import numpy as np
pygame.init()
font = pygame.font.SysFont("bahnschrift", 25)
class Tile:
  def __init__(self, is_mine=False):
    self.is_mine = is_mine
    self.is_flagged = False
    self.is_revealed = False
    self.adjacent_mines = 0
  def __str__(self):
     return f"{self.is_mine} {self.adjacent_mines}"
  
  def reveal(self):
    self.is_revealed = True
    print(self.adjacent_mines)
  
  

class Grid:
  def __init__(self, display):
    self.tileSize = 50
    self.grid = self.place_mines()
    self.display = display
    self.mineCount = 20
  
  def place_mines(self):
    rows,cols = 12,8

    grid = np.array([[Tile() for _ in range(rows)] for _ in range(cols)])
    flat_indices = np.random.choice(rows * cols, 20, replace=False)
    np.put(grid, flat_indices, [Tile(is_mine=True) for _ in range(20)])

    for i in range(rows):
      for j in range(cols):
          if not grid[j, i].is_mine:
            adjacent = self.get_adjacent_mines(grid,j,i)
            if adjacent != -1:
              grid[j, i].adjacent_mines = adjacent
    for i in grid:
      for j in i:
        if j.is_mine:
          print("M", end="  ")
        else:
          print(j.adjacent_mines,end="  ")
      print("")
    return grid
  

  def get_adjacent_mines(self, grid, x, y):
     adjacent_mines = 0
     if grid[x,y].is_mine:
        return -1
     else:
        for i in range(max(0, x - 1), min(8, x + 2)):
          for j in range(max(0, y - 1), min(12, y + 2)):
            if grid[i, j].is_mine:
              adjacent_mines += 1
        return adjacent_mines


  def draw_grid(self):
    for x in range(0,600,self.tileSize):
      for y in range(0,400,self.tileSize):
        rect = pygame.Rect(x, y, self.tileSize,self.tileSize)

        if x%(self.tileSize*2)==0 and y%(self.tileSize*2)==0 or x%(self.tileSize*2)!=0 and y%(self.tileSize*2)!=0:
          pygame.draw.rect(self.display,(64,64,64), rect)
        else:
          pygame.draw.rect(self.display,(32,32,32), rect)

class Game:
  def __init__(self):
    self.gameLoop = True
    self.display = pygame.display.set_mode((600,400))
    self.grid = Grid(self.display)

  def handle_click(self, x, y):
    gridX = x//50
    gridY = y//50
    print(gridX,gridY)
    self.grid.grid[gridY][gridX].reveal()

  def run_game(self):
    while self.gameLoop:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.gameLoop = False

        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = event.pos 
          self.handle_click(x,y)

      self.grid.draw_grid()
      pygame.display.update()
    print(self.grid.get_adjacent_mines(self.grid.grid, 2, 2))
if __name__ == "__main__":
  game = Game()
  game.run_game()