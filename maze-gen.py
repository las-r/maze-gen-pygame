import pygame
import random

# maze-gen.py made by las-r
# v1.0

# settings
DWIDTH, DHEIGHT = 600, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MWIDTH, MHEIGHT = 75, 75

# cell sizes
CWIDTH, CHEIGHT = DWIDTH // MWIDTH, DHEIGHT // MHEIGHT

# generate maze func
def gen():
    maze = [[1 for _ in range(MWIDTH)] for _ in range(MHEIGHT)]
    DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    stk = []
    sy, sx = random.randrange(1, MHEIGHT, 2), random.randrange(1, MWIDTH, 2)
    maze[sy][sx] = 0
    stk.append((sy, sx))
    while stk:
        y, x = stk[-1]
        random.shuffle(DIRS)
        moved = False
        for dy, dx in DIRS:
            ny, nx = y + dy, x + dx
            if 0 < ny < MHEIGHT - 1 and 0 < nx < MWIDTH - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                stk.append((ny, nx))
                moved = True
                draw(maze)
                break
        if not moved:
            stk.pop()
            
# draw maze func
def draw(maze):
    scr.fill(BLACK)
    for y in range(MHEIGHT):
        for x in range(MWIDTH):
            col = BLACK if maze[y][x] == 0 else WHITE
            pygame.draw.rect(scr, col, (x * CWIDTH, y * CHEIGHT, CWIDTH, CHEIGHT))
    pygame.display.flip()

# display
pygame.init()
scr = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("Maze Generator")

# generate
gen()

# input
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                gen()

# quit
pygame.quit()
