import pygame
import numpy as np
import time

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
      


class Grid:
  def __init__(self, display, topBarHeight=50):
    
    self.display = display
    self.tileSize = 25
    self.topBarHeight = topBarHeight + (self.display.get_height() % self.tileSize)
    print(self.topBarHeight, topBarHeight, self.display.get_height(), self.display.get_height() % self.tileSize, self.display.get_height()-topBarHeight / self.tileSize)
    self.rows = (self.display.get_height() - self.topBarHeight) // self.tileSize
    self.cols = self.display.get_width() // self.tileSize
    self.grid = np.array([[Tile() for _ in range(self.cols)] for _ in range(self.rows)])
    self.mineCount = (self.rows * self.cols) // 5
    self.placed = False
    self.width,self.height = self.display.get_size()
    self.tileColours = {
      1: (25, 118, 210),
      2: (56, 142, 60),
      3: (211, 47, 47),
      4: (123, 31, 162),
      5: (255, 143, 0),
      6: (0, 151, 167),
      7: (66, 66, 66),
      8: (158, 158, 158)
    }
    self.backgroundColours = {
      "lightUnrevealed": (166,217,73),
      "darkUnrevealed": (142,204,57),
      "lightRevealed": (229,195,158),
      "darkRevealed": (205,175,142)
    }
    self.flag = pygame.image.load("flag_icon.png")
    
    self.fontSize = int(self.tileSize)
    self.font = pygame.font.SysFont("bahnschrift",self.fontSize)
    self.flagCount = 0
    self.minesLeft = self.mineCount

  def initialize_grid(self,startingX, startingY):
    adjacent_coords = [(i,j)for i in range(max(0, startingY - 1), min(self.rows, startingY + 2)) for j in range(max(0, startingX - 1), min(self.cols, startingX + 2)) ]
    print(adjacent_coords)
    
    all_indices = np.arange(self.rows * self.cols)
    adjacent_indices = np.array([i * self.cols + j for i, j in adjacent_coords])
    valid_indices = np.setdiff1d(all_indices, adjacent_indices)

    mine_indices = np.random.choice(valid_indices, self.mineCount, replace=False)
    
    np.put(self.grid, mine_indices, [Tile(is_mine=True) for _ in range(self.mineCount)])
    
    for i in range(self.rows):
      for j in range(self.cols):
        if not self.grid[i][j].is_mine:
          adjacent = self.get_adjacent_mines(self.grid, j, i)
          if adjacent != -1:
            self.grid[i][j].adjacent_mines = adjacent
    self.placed = True
    

  def print_grid(self):
    for i in range(self.rows):
      for j in range(self.cols):
        if self.grid[i][j].is_mine:
          print("M", end="  ")
        else:
          print(self.grid[i][j].adjacent_mines, end="  ")
      print()
  def get_adjacent_mines(self, grid, x, y):
    adjacent_mines = 0
    if grid[y][x].is_mine:
      return -1
    else:
      for i in range(max(0, x - 1), min(self.cols, x + 2)):
        for j in range(max(0, y - 1), min(self.rows, y + 2)):
          if grid[j][i].is_mine:
            adjacent_mines += 1
    return adjacent_mines

  def check_win(self):
    for i in range(self.rows):
      for j in range(self.cols):
        if not self.grid[i][j].is_revealed and not self.grid[i][j].is_mine:
          return False
    return True
  def draw_top_bar(self,timer):

    pygame.draw.rect(self.display, (255, 255, 255), (0, 0, self.width, self.topBarHeight)) 
    text = self.font.render(str(timer), True, (0, 0, 0))
    self.display.blit(text, (self.width - 100, 0))
    text = self.font.render(str(self.mineCount-self.flagCount), True, (0, 0, 0))
    self.display.blit(text, (0, 0))
    
  def draw_grid(self,gameOver,timer):
    self.display.fill((0,0,0))
    for y in range(self.rows):
      for x in range(self.cols):
        rect = pygame.Rect(x * self.tileSize, y * self.tileSize + self.topBarHeight, self.tileSize, self.tileSize)
        tileX = x 
        tileY = y
        self.draw_top_bar(timer)
        if gameOver and self.grid[tileY][tileX].is_mine and not self.grid[tileY][tileX].is_flagged:
          self.grid[tileY][tileX].reveal()
        if self.grid[tileY][tileX].is_revealed:
          if (x + y) % 2 == 0:  # Simplified check for alternating colors
              print("drawing light at",x,y)
              pygame.draw.rect(self.display, self.backgroundColours["lightRevealed"], rect)
          else:
              print("drawing dark at",x,y)
              pygame.draw.rect(self.display, self.backgroundColours["darkRevealed"], rect)

          if self.grid[tileY][tileX].is_mine:
            pygame.draw.rect(self.display, (255,0,0), rect)
          else:
            adj = self.grid[tileY][tileX].adjacent_mines
            if adj > 0:
              text = self.font.render(str(adj), True, self.tileColours[adj])
              text_rect = text.get_rect(center=rect.center) 
              self.display.blit(text, text_rect)
        elif self.grid[tileY][tileX].is_flagged:
          flag = pygame.transform.scale(self.flag, (self.tileSize, self.tileSize))
          self.display.blit(flag, rect)
        else:
          if (x + y) % 2 == 0:
              print("drawing light at",x,y)
              pygame.draw.rect(self.display, self.backgroundColours["lightUnrevealed"], rect)
          else:
              print("drawing dark at",x,y)
              pygame.draw.rect(self.display, self.backgroundColours["darkUnrevealed"], rect)
                
  def reveal_adjacent(self, x, y):
    for i in range(max(0, x - 1), min(self.cols, x + 2)):
      for j in range(max(0, y - 1), min(self.rows, y + 2)):
        if not self.grid[j][i].is_revealed:
          self.grid[j][i].reveal()
          if self.grid[j][i].adjacent_mines == 0 and not self.grid[j][i].is_mine:
            self.reveal_adjacent(i, j)

class Game:
  def __init__(self):
    self.gameLoop = True
    self.gameOver  = False
    self.gameWon = False
    self.topBarHeight = 2
    self.width = 1250
    self.height = 750 
    self.timer = 0
    self.start_time = int(time.time())
    
    self.display = pygame.display.set_mode((self.width, self.height))
    self.grid = Grid(self.display,self.topBarHeight)

  def handle_click(self, button, x, y):
    
    gridX = (x // self.grid.tileSize) 
    gridY = ((y - self.topBarHeight) // self.grid.tileSize)
    print(gridX,gridY)
    if button == 1:
      
      if not self.grid.placed:
        self.grid.initialize_grid(gridX, gridY)
      if not self.grid.grid[gridY][gridX].is_flagged:
        self.grid.grid[gridY][gridX].reveal()
        if self.grid.grid[gridY][gridX].adjacent_mines == 0 and not self.grid.grid[gridY][gridX].is_mine:
          self.grid.reveal_adjacent(gridX, gridY)
        if self.grid.grid[gridY][gridX].is_mine:
          self.gameOver = True
        
        
    elif button == 3:
      if not self.grid.grid[gridY][gridX].is_revealed:
        self.grid.grid[gridY][gridX].is_flagged = not self.grid.grid[gridY][gridX].is_flagged
        self.grid.flagCount += 1 if self.grid.grid[gridY][gridX].is_flagged else -1

  def run_game(self):
    while self.gameLoop:
      if self.grid.check_win():
        self.gameWon = True
          
      if not self.gameOver and not self.gameWon:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.gameLoop = False
          if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.handle_click(event.button, x, y)
        self.grid.draw_grid(self.gameWon,self.timer)
        
        
      elif self.gameWon:         
        self.grid.draw_grid(self.gameOver, self.timer)
        pygame.display.update()
        text = font.render("You Win!", True, (0, 0, 0))
        self.display.blit(text, (self.width//2, self.height//2))
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.gameLoop = False
      else:
        self.grid.draw_grid(self.gameOver,self.timer)
        text = font.render("Game Over!", True, (0, 0, 0))
        self.display.blit(text, (self.width//2, self.height//2))
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.gameLoop = False
      
      if not self.gameOver and not self.gameWon:
        self.timer = int(time.time()) - self.start_time
      pygame.display.update()
if __name__ == "__main__":
  game = Game()
  game.run_game()