import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 4
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

# Clock
clock = pygame.time.Clock()

# Load images
def load_images():
    images = []
    for i in range(1, 9):
        img = pygame.image.load(f'images/img{i}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        images.append(img)
    return images

images = load_images()

def create_grid():
    grid = images * 2
    random.shuffle(grid)
    return [grid[i:i + GRID_SIZE] for i in range(0, len(grid), GRID_SIZE)]

grid = create_grid()
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

def get_tile(mouse_pos):
    x, y = mouse_pos
    return x // TILE_SIZE, y // TILE_SIZE

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if revealed[row][col]:
                screen.blit(grid[row][col], rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)

first_tile = None
second_tile = None
matches = 0

def check_for_match():
    global first_tile, second_tile, matches
    if grid[first_tile[1]][first_tile[0]] == grid[second_tile[1]][second_tile[0]]:
        revealed[first_tile[1]][first_tile[0]] = True
        revealed[second_tile[1]][second_tile[0]] = True
        matches += 1
    first_tile = None
    second_tile = None

running = True
while running:
    screen.fill(BLACK)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            tile = get_tile(mouse_pos)
            if not revealed[tile[1]][tile[0]]:
                if first_tile is None:
                    first_tile = tile
                elif second_tile is None:
                    second_tile = tile
                    check_for_match()
                else:
                    first_tile, second_tile = tile, None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
