"""
Pacman Game - Python/Pygame Port
Original Processing code converted to Python with same gameplay
"""

import pygame
import math
import random
import json
from typing import List, Optional
import os

# Initialize Pygame
pygame.init()

# ==========================================
# Load Configuration from JSON
# ==========================================
def load_config(config_path="pacman_config.json"):
    """Load configuration from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, config_path)
    
    with open(config_file, 'r') as f:
        return json.load(f)

CONFIG = load_config()

# Display settings
SC = CONFIG["display"]["scale"]
WIDTH = CONFIG["display"]["width"]
HEIGHT = CONFIG["display"]["height"]
FPS = CONFIG["display"]["fps"]
TITLE = CONFIG["display"]["title"]
ROWS = HEIGHT // SC
COLS = WIDTH // SC

# Colors (convert lists to tuples)
BACKGROUND = tuple(CONFIG["colors"]["background"])
WALL_COLOR = tuple(CONFIG["colors"]["wall"])
PATH_COLOR = tuple(CONFIG["colors"]["path"])
YELLOW = tuple(CONFIG["colors"]["pacman"])
FOOD_COLOR = tuple(CONFIG["colors"]["food"])
BLINKY_COLOR = tuple(CONFIG["colors"]["blinky"])
PINKY_COLOR = tuple(CONFIG["colors"]["pinky"])
INKY_COLOR = tuple(CONFIG["colors"]["inky"])
CLYDE_COLOR = tuple(CONFIG["colors"]["clyde"])
WEAK_COLOR = tuple(CONFIG["colors"]["weak"])
WEAK_ALPHA_COLOR = tuple(CONFIG["colors"]["weak"]) + (100,)

# Gameplay settings
PACMAN_SPEED = CONFIG["gameplay"]["pacman_speed"]
GHOST_SPEED = CONFIG["gameplay"]["ghost_speed"]
GHOST_WEAK_SPEED = CONFIG["gameplay"]["ghost_weak_speed"]
WEAK_DURATION = CONFIG["gameplay"]["weak_duration"]
SHOW_GHOST_PATHS = CONFIG["gameplay"]["show_ghost_paths"]

# Scoring
FOOD_POINTS = CONFIG["scoring"]["food_points"]
BONUS_POINTS = CONFIG["scoring"]["bonus_points"]
GHOST_POINTS = CONFIG["scoring"]["ghost_points"]

# Game map
# '0' = free, '1' = wall, '2' = food, '3' = bonus, '-' = teleport
MAP = [
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '3', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '3', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '0', '0', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['-', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '-'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '2', '1'],
    ['1', '3', '2', '2', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '3', '1'],
    ['1', '1', '1', '2', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '2', '1', '1', '1'],
    ['1', '1', '1', '2', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '2', '1', '1', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1'],
    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
]


class Cell:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        self.f = float('inf')
        self.g = 0
        self.h = 0
        self.parent: Optional['Cell'] = None
        self.is_wall = False

    def reset_cell(self):
        self.f = float('inf')
        self.g = 0
        self.h = 0
        self.parent = None


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Load background image
        self.background = None
        # Try multiple paths for the image
        data_dir = os.path.join(os.path.dirname(__file__), "Pacman", "Image")
        possible_paths = [
            os.path.join(data_dir, "PacmanBoard.png"),
            os.path.join(os.path.dirname(__file__), "Image", "PacmanBoard.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sketch", "Image", "PacmanBoard.png"),
        ]
        for img_path in possible_paths:
            if os.path.exists(img_path):
                self.background = pygame.image.load(img_path)
                break
        
        # Load ghost images
        self.ghost_images = {}
        ghost_size = SC + 4
        ghost_files = {
            'blinky': 'Blinky.png',
            'pinky': 'Pinky.png',
            'inky': 'Inky.png',
            'clyde': 'Clyde.png'
        }
        for name, filename in ghost_files.items():
            img_path = os.path.join(data_dir, filename)
            if os.path.exists(img_path):
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (ghost_size, ghost_size))
                self.ghost_images[name] = img
            else:
                self.ghost_images[name] = None
        
        # Load Pacman image
        pacman_size = 24  # Slightly larger than SC
        pacman_path = os.path.join(data_dir, 'pacman.png')
        if os.path.exists(pacman_path):
            self.pacman_image = pygame.image.load(pacman_path)
            self.pacman_image = pygame.transform.scale(self.pacman_image, (pacman_size, pacman_size))
        else:
            self.pacman_image = None
        
        # Initialize grid
        self.array: List[List[Cell]] = []
        self.food: List[Cell] = []
        self.bonus_food: List[Cell] = []
        self.path: List[Cell] = []
        
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                cell = Cell(i, j)
                if MAP[i][j] == '1':
                    cell.is_wall = True
                elif MAP[i][j] == '2':
                    self.food.append(cell)
                elif MAP[i][j] == '3':
                    self.bonus_food.append(cell)
                row.append(cell)
            self.array.append(row)
        
        # Initialize Pacman
        self.pacman = PacMan(self)
        
        # Initialize Ghosts
        self.blinky = Blinky(self, 13, 13, BLINKY_COLOR)
        self.pinky = Pinky(self, 14, 13, PINKY_COLOR)
        self.inky = Inky(self, 14, 12, INKY_COLOR)
        self.clyde = Clyde(self, 14, 14, CLYDE_COLOR)
        
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        
        self.running = True
        self.game_over = False
        self.won = False

    def heuristic(self, a: Cell, b: Cell) -> float:
        return math.sqrt((a.j - b.j) ** 2 + (a.i - b.i) ** 2)

    def get_successors(self, cell: Cell) -> List[Cell]:
        successors = []
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # up, left, down, right
        
        for di, dj in directions:
            ni, nj = cell.i + di, cell.j + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                neighbor = self.array[ni][nj]
                if not neighbor.is_wall:
                    successors.append(neighbor)
        return successors

    def reset_parents(self):
        for i in range(ROWS):
            for j in range(COLS):
                self.array[i][j].reset_cell()

    def a_star(self, start: Cell, end: Cell):
        open_list: List[Cell] = []
        closed_list: List[Cell] = []
        self.path = []
        
        self.reset_parents()
        
        open_list.append(start)
        start.f = 0
        
        while open_list:
            # Find cell with lowest f
            q = min(open_list, key=lambda c: c.f)
            open_list.remove(q)
            
            successors = self.get_successors(q)
            
            for s in successors:
                if s not in closed_list:
                    if s == end:
                        s.parent = q
                        self.get_path(q)
                        return
                    
                    new_g = q.g + 1
                    new_h = self.heuristic(s, end)
                    new_f = new_g + new_h
                    
                    if s.f == float('inf') or s.f > new_f:
                        open_list.append(s)
                        s.f = new_f
                        s.g = new_g
                        s.h = new_h
                        s.parent = q
            
            closed_list.append(q)

    def get_path(self, q: Cell):
        temp = q
        self.path.append(temp)
        while temp.parent is not None:
            self.path.append(temp.parent)
            temp = temp.parent

    def draw_coins(self):
        offset_x = SC // 2
        offset_y = SC // 2
        
        for cell in self.food:
            pygame.draw.circle(self.screen, FOOD_COLOR, 
                             (cell.j * SC + offset_x, cell.i * SC + offset_y), 3)
        
        for cell in self.bonus_food:
            pygame.draw.circle(self.screen, FOOD_COLOR, 
                             (cell.j * SC + offset_x, cell.i * SC + offset_y), 8)
        
        if len(self.food) == 0 and len(self.bonus_food) == 0:
            self.won = True
            self.game_over = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pacman.change_dir(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.change_dir(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.change_dir(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.change_dir(-1, 0)
                    elif event.key == pygame.K_RETURN and self.game_over:
                        # Restart game
                        self.__init__()
            
            if not self.game_over:
                self.update()
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

    def update(self):
        # Update Pacman
        self.pacman.update()
        
        # Handle ghost power-up state
        if self.pacman.is_invincible:
            for ghost in self.ghosts:
                if not ghost.is_weak and not ghost.is_recovering and ghost.is_affected_by:
                    ghost.make_weak()
        else:
            for ghost in self.ghosts:
                if ghost.is_weak:
                    ghost.make_normal()
        
        # Check collisions with ghosts
        for ghost in self.ghosts:
            if (abs(self.pacman.x - ghost.x) < SC + 10 and 
                abs(self.pacman.y - ghost.y) < SC + 10):
                if self.pacman.is_invincible and ghost.is_affected_by:
                    ghost.retreat()
                else:
                    print(f"Caught by {ghost.__class__.__name__}")
                    self.game_over = True
                    return
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.search()

    def draw(self):
        self.screen.fill(BACKGROUND)
        
        # Draw background
        # Use custom wall drawing instead of image
        self.draw_walls()
        
        # Draw food
        self.draw_coins()
        
        # Draw Pacman
        self.pacman.draw()
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw()
        
        # Game over message
        if self.game_over:
            font = pygame.font.Font(None, 74)
            if self.won:
                text = font.render("You Win!", True, (100, 255, 150))
            else:
                text = font.render("End Game", True, (255, 100, 100))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Enter to Restart", True, (255, 220, 50))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

    def draw_walls(self):
        """Fallback wall drawing if image not found"""
        for i in range(ROWS):
            for j in range(COLS):
                if MAP[i][j] == '1':
                    # Draw dark wall block
                    pygame.draw.rect(self.screen, WALL_COLOR,
                                   (j * SC, i * SC, SC, SC))
                else:
                    # Draw light path
                    pygame.draw.rect(self.screen, PATH_COLOR,
                                   (j * SC, i * SC, SC, SC))
                    # Draw subtle grid lines
                    pygame.draw.rect(self.screen, (140, 150, 165),
                                   (j * SC, i * SC, SC, SC), 1)


class PacMan:
    def __init__(self, game: Game):
        self.game = game
        self.x = 12 * SC
        self.y = 23 * SC
        self.dir_x = -1
        self.dir_y = 0
        self.new_dir_x = -1
        self.new_dir_y = 0
        self.speed = PACMAN_SPEED
        self.i = 23
        self.j = 12
        self.is_invincible = False
        self.countdown = 600
        self.current_cell = game.array[23][12]

    def update(self):
        # Snap to grid when close enough (fixes floating point precision issues)
        if abs(self.x % SC) < self.speed or abs(self.x % SC) > SC - self.speed:
            self.x = round(self.x / SC) * SC
        if abs(self.y % SC) < self.speed or abs(self.y % SC) > SC - self.speed:
            self.y = round(self.y / SC) * SC
        
        if self.x % 20 == 0 and self.y % 20 == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Eat food
            current = self.game.array[self.i][self.j]
            if current in self.game.food:
                self.game.food.remove(current)
            
            # Check bonus food
            if self.check_bonus():
                self.is_invincible = True
                self.countdown = 600
            
            # Teleport
            if MAP[self.i][self.j] == '-' and self.j == 0:
                self.x = 27 * SC
                self.j = 27
            elif MAP[self.i][self.j] == '-' and self.j == 27:
                self.x = 0
                self.j = 0
            
            # Check next position
            next_x = self.j + self.dir_x
            next_y = self.i + self.dir_y
            
            if 0 <= next_y < ROWS and 0 <= next_x < COLS:
                if MAP[next_y][next_x] == '1':
                    self.dir_x = 0
                    self.dir_y = 0
            
            # Check new direction
            new_x = self.j + self.new_dir_x
            new_y = self.i + self.new_dir_y
            
            if 0 <= new_y < ROWS and 0 <= new_x < COLS:
                if MAP[new_y][new_x] != '1':
                    self.dir_x = self.new_dir_x
                    self.dir_y = self.new_dir_y
            
            self.current_cell = self.game.array[self.i][self.j]
        
        # Invincibility countdown
        if self.is_invincible:
            if self.countdown > 0:
                self.countdown -= 1
            else:
                self.is_invincible = False
        
        # Move
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self):
        offset_x = SC // 2
        offset_y = SC // 2
        pacman_size = 24
        
        if self.game.pacman_image:
            # Rotate image based on direction
            img = self.game.pacman_image
            if self.dir_x == 1:  # Right
                img = self.game.pacman_image
            elif self.dir_x == -1:  # Left
                img = pygame.transform.flip(self.game.pacman_image, True, False)
            elif self.dir_y == -1:  # Up
                img = pygame.transform.rotate(self.game.pacman_image, 90)
            elif self.dir_y == 1:  # Down
                img = pygame.transform.rotate(self.game.pacman_image, -90)
            
            self.game.screen.blit(img, 
                                 (int(self.x) + offset_x - pacman_size // 2,
                                  int(self.y) + offset_y - pacman_size // 2))
        else:
            # Fallback to yellow circle
            pygame.draw.circle(self.game.screen, YELLOW, 
                              (int(self.x) + offset_x, int(self.y) + offset_y), 12)

    def change_dir(self, dir_x: int, dir_y: int):
        self.new_dir_x = dir_x
        self.new_dir_y = dir_y

    def check_bonus(self) -> bool:
        current = self.game.array[self.i][self.j]
        if current in self.game.bonus_food:
            for ghost in self.game.ghosts:
                ghost.is_affected_by = True
            self.game.bonus_food.remove(current)
            return True
        return False


class Ghost:
    def __init__(self, game: Game, i: int, j: int, color: tuple, ghost_name: str = 'ghost'):
        self.game = game
        self.x = j * SC
        self.y = i * SC
        self.i = i
        self.j = j
        self.speed = GHOST_SPEED
        self.dir_x = 1
        self.dir_y = 0
        self.color = color
        self.ghost_name = ghost_name
        self.current_cell = game.array[i][j] if i < len(game.array) and j < len(game.array[0]) else None
        self.cell_to_follow = self.get_random_cell()
        self.searching_list: List[Cell] = []
        
        # Ghost house cells
        self.ghost_house_cells: List[Cell] = []
        for k in range(13, 16):
            for l in range(11, 17):
                if k < ROWS and l < COLS:
                    self.ghost_house_cells.append(game.array[k][l])
        
        self.is_weak = False
        self.is_recovering = False
        self.is_affected_by = False
        self.recovering_countdown = 720

    def update(self):
        # Snap to grid when close enough (fixes floating point precision issues)
        if abs(self.x % SC) < self.speed or abs(self.x % SC) > SC - self.speed:
            self.x = round(self.x / SC) * SC
        if abs(self.y % SC) < self.speed or abs(self.y % SC) > SC - self.speed:
            self.y = round(self.y / SC) * SC
        
        if self.x % SC == 0 and self.y % SC == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Bounds check
            if not (0 <= self.i < ROWS and 0 <= self.j < COLS):
                self.dir_x, self.dir_y = 0, 0
                return
            
            # Determine direction from searching list
            up = self.game.array[self.i - 1][self.j] if self.i > 0 else None
            left = self.game.array[self.i][self.j - 1] if self.j > 0 else None
            down = self.game.array[self.i + 1][self.j] if self.i < ROWS - 1 else None
            right = self.game.array[self.i][self.j + 1] if self.j < COLS - 1 else None
            
            if up and up in self.searching_list:
                self.dir_x, self.dir_y = 0, -1
            elif left and left in self.searching_list:
                self.dir_x, self.dir_y = -1, 0
            elif down and down in self.searching_list:
                self.dir_x, self.dir_y = 0, 1
            elif right and right in self.searching_list:
                self.dir_x, self.dir_y = 1, 0
            
            # Check for wall before moving
            next_i = self.i + self.dir_y
            next_j = self.j + self.dir_x
            if 0 <= next_i < ROWS and 0 <= next_j < COLS:
                if MAP[next_i][next_j] == '1':
                    self.dir_x, self.dir_y = 0, 0
            else:
                self.dir_x, self.dir_y = 0, 0
        
        # Adjust speed when weak
        if (self.is_weak or self.is_recovering) and self.is_affected_by:
            self.speed = GHOST_WEAK_SPEED
        else:
            self.speed = GHOST_SPEED
        
        # Recovery countdown
        if self.is_recovering:
            if self.recovering_countdown == 0:
                self.recovering_countdown = 720
                self.is_recovering = False
                self.is_affected_by = False
            else:
                self.recovering_countdown -= 1
        
        # Move
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self):
        offset_x = SC // 2
        offset_y = SC // 2
        ghost_size = SC + 4
        
        # Get ghost image
        ghost_img = self.game.ghost_images.get(self.ghost_name)
        
        if self.is_weak or self.is_recovering:
            # Draw blue circle for weak/recovering state
            if self.is_recovering:
                # Create a surface with alpha for semi-transparency
                surface = pygame.Surface((ghost_size, ghost_size), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*WEAK_COLOR, 100), 
                                 (ghost_size // 2, ghost_size // 2), ghost_size // 2)
                self.game.screen.blit(surface, 
                                     (int(self.x) + offset_x - ghost_size // 2,
                                      int(self.y) + offset_y - ghost_size // 2))
            else:
                pygame.draw.circle(self.game.screen, WEAK_COLOR,
                                 (int(self.x) + offset_x, int(self.y) + offset_y), ghost_size // 2)
        elif ghost_img:
            # Draw ghost image
            self.game.screen.blit(ghost_img, 
                                 (int(self.x) + offset_x - ghost_size // 2,
                                  int(self.y) + offset_y - ghost_size // 2))
        else:
            # Fallback to colored circle if image not found
            pygame.draw.circle(self.game.screen, self.color,
                             (int(self.x) + offset_x, int(self.y) + offset_y), ghost_size // 2)

    def draw_path(self):
        if len(self.searching_list) < 2:
            return
        
        offset_x = SC // 2
        offset_y = SC // 2
        
        if self.is_weak:
            color = WEAK_COLOR
        elif self.is_recovering:
            color = (27, 112, 247)
        else:
            color = self.color
        
        points = [(cell.j * SC + offset_x, cell.i * SC + offset_y) for cell in self.searching_list]
        
        # Replace last point with ghost position
        if len(points) > 1:
            points[-1] = (int(self.x) + offset_x, int(self.y) + offset_y)
        
        for i in range(len(points) - 1):
            pygame.draw.line(self.game.screen, color, points[i], points[i + 1], 3)

    def make_weak(self):
        if not self.is_weak and self.is_affected_by:
            self.cell_to_follow = self.get_random_cell()
            self.is_weak = True

    def make_normal(self):
        if self.is_weak:
            self.is_weak = False
            self.is_affected_by = False

    def retreat(self):
        if not self.is_recovering and self.is_affected_by:
            self.is_recovering = True
            self.is_weak = False
            self.cell_to_follow = self.get_random_cell_from_house()

    def get_random_cell(self) -> Cell:
        i, j = 0, 0
        while MAP[i][j] == '1':
            i = random.randint(0, ROWS - 1)
            j = random.randint(0, COLS - 1)
        return self.game.array[i][j]

    def get_random_cell_from_house(self) -> Cell:
        if self.ghost_house_cells:
            return random.choice(self.ghost_house_cells)
        return self.get_random_cell()

    def get_cell_in_front_of(self, n: int) -> Cell:
        pacman = self.game.pacman
        i = pacman.i + pacman.dir_y
        j = pacman.j + pacman.dir_x
        
        if not (0 <= i < ROWS and 0 <= j < COLS):
            return self.get_random_cell()
        
        initial = self.game.array[pacman.i][pacman.j]
        root = self.game.array[i][j]
        
        for _ in range(n):
            positions = []
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            
            for di, dj in directions:
                ni, nj = root.i + di, root.j + dj
                if 0 <= ni < ROWS and 0 <= nj < COLS:
                    cell = self.game.array[ni][nj]
                    if not cell.is_wall:
                        positions.append(cell)
            
            if initial in positions:
                positions.remove(initial)
            
            initial = root
            
            if positions:
                root = random.choice(positions)
            else:
                return self.get_random_cell()
        
        return root

    def search(self):
        """Override in subclasses"""
        pass


class Blinky(Ghost):
    """Blinky always chases Pacman directly"""
    
    def __init__(self, game: Game, i: int, j: int, color: tuple):
        super().__init__(game, i, j, color, 'blinky')
    
    def search(self):
        if self.x % SC == 0 and self.y % SC == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Bounds checking
            if not (0 <= self.i < ROWS and 0 <= self.j < COLS):
                self.update()
                return
            
            self.current_cell = self.game.array[self.i][self.j]
            
            if (self.is_weak or self.is_recovering) and self.is_affected_by:
                if len(self.searching_list) <= 2:
                    if self.is_weak:
                        self.cell_to_follow = self.get_random_cell()
                    elif self.is_recovering:
                        self.cell_to_follow = self.get_random_cell_from_house()
            else:
                # Chase Pacman directly
                self.cell_to_follow = self.game.pacman.current_cell
            
            self.game.a_star(self.current_cell, self.cell_to_follow)
            self.searching_list = self.game.path.copy()
        
        self.update()


class Pinky(Ghost):
    """Pinky tries to ambush Pacman"""
    
    def __init__(self, game: Game, i: int, j: int, color: tuple):
        super().__init__(game, i, j, color, 'pinky')
        self.new_search = 8

    def search(self):
        if self.x % SC == 0 and self.y % SC == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Bounds checking
            if not (0 <= self.i < ROWS and 0 <= self.j < COLS):
                self.update()
                return
            
            self.new_search -= 1
            
            self.current_cell = self.game.array[self.i][self.j]
            
            if (self.is_weak or self.is_recovering) and self.is_affected_by:
                self.new_search = 1
                if len(self.searching_list) <= 2:
                    if self.is_weak:
                        self.cell_to_follow = self.get_random_cell()
                    elif self.is_recovering:
                        self.cell_to_follow = self.get_random_cell_from_house()
            else:
                # Try to get ahead of Pacman
                if self.new_search == 0:
                    self.cell_to_follow = self.get_cell_in_front_of(6)
                    self.new_search = 8
            
            self.game.a_star(self.current_cell, self.cell_to_follow)
            self.searching_list = self.game.path.copy()
        
        self.update()


class Inky(Ghost):
    """Inky uses Blinky's position to determine target"""
    
    def __init__(self, game: Game, i: int, j: int, color: tuple):
        super().__init__(game, i, j, color, 'inky')
    
    def search(self):
        if self.x % SC == 0 and self.y % SC == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Bounds checking
            if not (0 <= self.i < ROWS and 0 <= self.j < COLS):
                self.update()
                return
            
            self.current_cell = self.game.array[self.i][self.j]
            
            if (self.is_weak or self.is_recovering) and self.is_affected_by:
                if len(self.searching_list) <= 2:
                    if self.is_weak:
                        self.cell_to_follow = self.get_random_cell()
                    elif self.is_recovering:
                        self.cell_to_follow = self.get_random_cell_from_house()
            else:
                # Use Blinky's position
                pacman = self.game.pacman
                blinky = self.game.blinky
                possible_i = 2 * pacman.i - blinky.i
                possible_j = 2 * pacman.j - blinky.j
                
                if (0 <= possible_i < ROWS and 0 <= possible_j < COLS and
                    not self.game.array[possible_i][possible_j].is_wall):
                    self.cell_to_follow = self.game.array[possible_i][possible_j]
                elif len(self.searching_list) <= 2:
                    self.cell_to_follow = self.get_random_cell()
            
            self.game.a_star(self.current_cell, self.cell_to_follow)
            self.searching_list = self.game.path.copy()
        
        self.update()


class Clyde(Ghost):
    """Clyde searches for tile far from Pacman"""
    
    def __init__(self, game: Game, i: int, j: int, color: tuple):
        super().__init__(game, i, j, color, 'clyde')
        self.new_search = 10

    def search(self):
        if self.x % SC == 0 and self.y % SC == 0:
            self.i = int(self.y) // SC
            self.j = int(self.x) // SC
            
            # Bounds checking
            if not (0 <= self.i < ROWS and 0 <= self.j < COLS):
                self.update()
                return
            
            self.new_search -= 1
            
            self.current_cell = self.game.array[self.i][self.j]
            
            if (self.is_weak or self.is_recovering) and self.is_affected_by:
                self.new_search = 1
                if len(self.searching_list) <= 2:
                    if self.is_weak:
                        self.cell_to_follow = self.get_random_cell()
                    elif self.is_recovering:
                        self.cell_to_follow = self.get_random_cell_from_house()
            else:
                # Get cell far ahead
                if self.new_search == 0:
                    self.cell_to_follow = self.get_cell_in_front_of(12)
                    self.new_search = 10
            
            self.game.a_star(self.current_cell, self.cell_to_follow)
            self.searching_list = self.game.path.copy()
        
        self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
