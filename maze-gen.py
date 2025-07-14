import pygame
import random

# maze-gen.py made by las-r
# v1.1

# settings
DWIDTH, DHEIGHT = 600, 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
MWIDTH, MHEIGHT = 75, 75

# cell sizes
CWIDTH, CHEIGHT = DWIDTH // MWIDTH, DHEIGHT // MHEIGHT

# finished flag
f = False

# generate maze func
def gen():
    global f, maze, sy, sx, ny, nx, stk
    
    # initial maze (0 is path, 1 is wall, 2 is solver path)
    maze = [[1 for _ in range(MWIDTH)] for _ in range(MHEIGHT)]
    maze[0][1] = 0
    maze[-1][-2] = 0
    
    # solving prereqs
    DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    stk = []
    
    # starting cell
    sy, sx = random.randrange(1, MHEIGHT, 2), random.randrange(1, MWIDTH, 2)
    maze[sy][sx] = 0
    stk.append((sy, sx))
    
    # dfs loop
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
                draw()
                break
        if not moved:
            stk.pop()
    f = True
            
# draw maze func
def draw():
    # clear display buffer
    scr.fill(BLACK)
    
    # draw each cell
    for y in range(MHEIGHT):
        for x in range(MWIDTH):
            # colors
            if maze[y][x] == 1:
                col = WHITE
            elif maze[y][x] == 2:
                col = RED
            elif not f:
                if (y, x) == (sy, sx):
                    col = GREEN
                else:
                    col = BLACK
            else:
                col = BLACK
                
            # draw cell rect
            pygame.draw.rect(scr, col, (x * CWIDTH, y * CHEIGHT, CWIDTH, CHEIGHT))
            
    # flip buffer
    pygame.display.flip()
    
# solve maze func
def solve():
    global maze
    
    # starting pos and dir
    y, x = 0, 1
    cdir = "s"

    # direction functions
    def right(dir):
        return {"n": "e", "e": "s", "s": "w", "w": "n"}[dir]
    def left(dir):
        return {"n": "w", "w": "s", "s": "e", "e": "n"}[dir]
    def back(dir):
        return {"n": "s", "s": "n", "e": "w", "w": "e"}[dir]

    # move function
    def move(y, x, sdir):
        if sdir == "n": return y - 1, x
        if sdir == "s": return y + 1, x
        if sdir == "e": return y, x + 1
        if sdir == "w": return y, x - 1

    # rhr loop
    while (y, x) != (MHEIGHT - 1, MWIDTH - 2):
        maze[y][x] = 2
        draw()

        # try directions
        rdir = right(cdir)
        ry, rx = move(y, x, rdir) # type: ignore
        if maze[ry][rx] != 1:
            y, x = ry, rx
            cdir = rdir
            continue
        fy, fx = move(y, x, cdir) # type: ignore
        if maze[fy][fx] != 1:
            y, x = fy, fx
            continue
        ldir = left(cdir)
        ly, lx = move(y, x, ldir) # type: ignore
        if maze[ly][lx] != 1:
            y, x = ly, lx
            cdir = ldir
            continue
        bdir = back(cdir)
        by, bx = move(y, x, bdir) # type: ignore
        y, x = by, bx
        cdir = bdir

    # draw path
    maze[y][x] = 2
    draw()

# pygame display
pygame.init()
scr = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("Maze Generator")

# create maze
gen()
draw()

# input
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            # restart
            if e.key == pygame.K_r:
                f = False
                gen()
                draw()
            
            # solve
            elif e.key == pygame.K_s:
                solve()

# quit
pygame.quit()
