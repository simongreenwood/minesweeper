import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (138, 43, 226)  # Color for superfood

# Screen dimensions
dis_width = 600
dis_height = 400

# Set the clock for controlling the game's speed
clock = pygame.time.Clock()

# Snake settings
snake_block = 10
snake_speed = 15

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


class Snake:
    def __init__(self):
        self.snake_block = snake_block
        self.snake_List = []
        self.Length_of_snake = 1
        self.x = dis_width // 2
        self.y = dis_height // 2
        self.x_change = 0
        self.y_change = 0

    def move(self):
        """Update snake's position based on the direction."""
        self.x += self.x_change
        self.y += self.y_change

    def grow(self, growth=1):
        """Increase the length of the snake by a certain amount (default 1)."""
        self.Length_of_snake += growth

    def update_snake(self):
        """Add the current position of the snake's head to the snake list."""
        snake_Head = [self.x, self.y]
        self.snake_List.append(snake_Head)
        if len(self.snake_List) > self.Length_of_snake:
            del self.snake_List[0]

    def check_collision(self):
        """Check if the snake collides with itself."""
        for segment in self.snake_List[:-1]:
            if segment == [self.x, self.y]:
                return True
        return False

    def draw_snake(self, dis):
        """Draw the snake on the screen."""
        for segment in self.snake_List:
            pygame.draw.rect(dis, black, [segment[0], segment[1], self.snake_block, self.snake_block])


class Food:
    def __init__(self):
        self.x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        self.y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        self.color = green  # Default color for regular food

    def spawn_new_food(self):
        """Generate new food at a random position."""
        self.x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        self.y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    def draw_food(self, dis):
        """Draw food on the screen."""
        pygame.draw.rect(dis, self.color, [self.x, self.y, snake_block, snake_block])


class Superfood(Food):
    def __init__(self):
        super().__init__()
        self.color = purple  # Superfood color


class Game:
    def __init__(self):
        self.dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Snake Game by ChatGPT')
        self.snake = Snake()
        self.food_list = [Food()]  # List of foods, starts with 1 regular food
        self.game_over = False
        self.game_close = False

    def display_score(self, score):
        """Display the score on the screen."""
        value = score_font.render("Your Score: " + str(score), True, yellow)
        self.dis.blit(value, [0, 0])

    def display_message(self, msg, color):
        """Display a message on the screen."""
        mesg = font_style.render(msg, True, color)
        self.dis.blit(mesg, [dis_width / 6, dis_height / 3])

    def handle_key_events(self):
        """Handle key events for the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake.x_change == 0:
                    self.snake.x_change = -snake_block
                    self.snake.y_change = 0
                elif event.key == pygame.K_RIGHT and self.snake.x_change == 0:
                    self.snake.x_change = snake_block
                    self.snake.y_change = 0
                elif event.key == pygame.K_UP and self.snake.y_change == 0:
                    self.snake.y_change = -snake_block
                    self.snake.x_change = 0
                elif event.key == pygame.K_DOWN and self.snake.y_change == 0:
                    self.snake.y_change = snake_block
                    self.snake.x_change = 0

    def spawn_food(self):
        """Spawn new food, possibly a superfood or two foods."""
        # 1 in 3 chance to spawn a superfood
        if random.randint(1, 3) == 1:
            self.food_list.append(Superfood())
        else:
            self.food_list.append(Food())

        # 1 in 10 chance to spawn 2 foods
        if random.randint(1, 10) == 1:
            self.food_list.append(Food())

    def run_game(self):
        """Run the main game loop."""
        while not self.game_over:

            while self.game_close:
                self.dis.fill(blue)
                self.display_message("You Lost! Press Q-Quit or C-Play Again", red)
                self.display_score(self.snake.Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            self.__init__()  # Restart game

            self.handle_key_events()

            # Check for boundary collision
            if self.snake.x >= dis_width or self.snake.x < 0 or self.snake.y >= dis_height or self.snake.y < 0:
                self.game_close = True

            # Move the snake
            self.snake.move()
            self.snake.update_snake()

            # Check if the snake collides with itself
            if self.snake.check_collision():
                self.game_close = True

            # Draw the game
            self.dis.fill(blue)
            for food in self.food_list:
                food.draw_food(self.dis)
            self.snake.draw_snake(self.dis)
            self.display_score(self.snake.Length_of_snake - 1)

            pygame.display.update()

            # Check if snake eats any food
            for food in self.food_list[:]:  # Iterate over a copy to allow modification
                if self.snake.x == food.x and self.snake.y == food.y:
                    if isinstance(food, Superfood):
                        self.snake.grow(3)  # Superfood gives 3 points
                    else:
                        self.snake.grow(1)
                    self.food_list.remove(food)  # Remove the eaten food
                    self.spawn_food()  # Spawn new food

            # Control the speed of the game
            clock.tick(snake_speed)

        pygame.quit()
        quit()


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run_game()