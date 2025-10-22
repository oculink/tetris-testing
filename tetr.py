import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

class Tetromino:
    def __init__(self, shape_name):
        self.shape_name = shape_name
        self.shape = SHAPES[shape_name]
        self.color = COLORS[shape_name]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500
        
    def new_piece(self):
        return Tetromino(random.choice(list(SHAPES.keys())))
    
    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True
    
    def lock_piece(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_piece.x + j
                    y = self.current_piece.y + i
                    if y >= 0:
                        self.grid[y][x] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self.new_piece()
        
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True
    
    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        
        if lines_cleared:
            self.score += lines_cleared * 100 * lines_cleared
    
    def move(self, dx, dy):
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        
        if self.valid_move(self.current_piece, new_x, new_y):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            return True
        return False
    
    def rotate_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = original_shape
    
    def drop_piece(self):
        while self.move(0, 1):
            pass
        self.lock_piece()
    
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def draw_piece(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = (self.current_piece.x + j) * GRID_SIZE
                    y = (self.current_piece.y + i) * GRID_SIZE
                    rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(self.screen, self.current_piece.color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        font = pygame.font.Font(None, 48)
        text = font.render('GAME OVER', True, RED)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        
        font_small = pygame.font.Font(None, 24)
        restart_text = font_small.render('Press R to restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def reset(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
    
    def run(self):
        running = True
        
        while running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                    else:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.drop_piece()
            
            if not self.game_over and self.fall_time >= self.fall_speed:
                if not self.move(0, 1):
                    self.lock_piece()
                self.fall_time = 0
            
            self.screen.fill(BLACK)
            self.draw_grid()
            if not self.game_over:
                self.draw_piece()
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
