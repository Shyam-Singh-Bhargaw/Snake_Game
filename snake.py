# Let's begin building an enhanced version of the Snake Game using Pygame with improved visuals,
# smoother transitions, cleaner UI/UX, and light animations. This will keep the structure modular and polished.

import pygame
import random
import sys
import traceback

# Configurations
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10  # Slower speed for better gameplay

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (30, 144, 255)
DARK_GRAY = (30, 30, 30)
YELLOW = (255, 215, 0)

CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("🐍 Enhanced Snake Game")
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.large_font = pygame.font.SysFont("consolas", 48, bold=True)

        self.running = True
        self.game_active = False
        self.game_over = False
        self.score = 0
        self.snake = []
        self.food = {}
        self.direction = 'RIGHT'
        self.start_button = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 60, 160, 50)
        self.reset()

    def reset(self):
        self.snake = [{'x': CELL_WIDTH // 2, 'y': CELL_HEIGHT // 2}]
        self.direction = 'RIGHT'
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.game_active = False

    def spawn_food(self):
        while True:
            pos = {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}
            if pos not in self.snake:
                return pos

    def draw_cell(self, x, y, color, border_color=BLACK):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.window, color, rect)
        pygame.draw.rect(self.window, border_color, rect, 1)

    def draw_snake(self):
        for idx, segment in enumerate(self.snake):
            color = GREEN if idx != 0 else YELLOW
            self.draw_cell(segment['x'], segment['y'], color)

    def draw_food(self):
        self.draw_cell(self.food['x'], self.food['y'], RED)

    def draw_score(self):
        score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
        self.window.blit(score_surface, (10, 10))

    def show_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GRAY)
        self.window.blit(overlay, (0, 0))

        game_over_text = self.large_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, BLUE)

        self.window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 80))
        self.window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
        self.window.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

    def show_start_screen(self):
        self.window.fill(DARK_GRAY)
        title = self.large_font.render("🐍 Snake Game", True, GREEN)
        instructions = self.font.render("Use W/A/S/D or Arrow keys to move.", True, WHITE)
        click_text = self.font.render("Click Start to begin!", True, WHITE)

        pygame.draw.rect(self.window, BLUE, self.start_button, border_radius=8)
        start_text = self.font.render("Start", True, WHITE)
        self.window.blit(start_text, (
            self.start_button.centerx - start_text.get_width() // 2,
            self.start_button.centery - start_text.get_height() // 2)
        )

        self.window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 120))
        self.window.blit(instructions, (WINDOW_WIDTH // 2 - instructions.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        self.window.blit(click_text, (WINDOW_WIDTH // 2 - click_text.get_width() // 2, WINDOW_HEIGHT // 2 - 20))
        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                if self.start_button.collidepoint(event.pos):
                    self.game_active = True

            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.running = False
                elif self.game_active:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

    def update(self):
        if not self.game_active or self.game_over:
            return

        head = self.snake[0].copy()
        if self.direction == 'UP':
            head['y'] -= 1
        elif self.direction == 'DOWN':
            head['y'] += 1
        elif self.direction == 'LEFT':
            head['x'] -= 1
        elif self.direction == 'RIGHT':
            head['x'] += 1

        if head['x'] < 0 or head['x'] >= CELL_WIDTH or head['y'] < 0 or head['y'] >= CELL_HEIGHT or head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def render(self):
        self.window.fill(BLACK)

        if not self.game_active:
            self.show_start_screen()
            return

        self.draw_snake()
        self.draw_food()
        self.draw_score()

        if self.game_over:
            self.show_game_over()

        pygame.display.update()

    def run(self):
        try:
            while self.running:
                self.handle_input()
                self.update()
                self.render()
                self.clock.tick(FPS)
        except Exception as e:
            print("💥 ERROR:", str(e))
            traceback.print_exc()
        finally:
            pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()

