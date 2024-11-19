import pygame 
import sys
import random



#TODO: use take_action for rl algo
#TODO: create game class for game instance and management
#TODO: create fields to share with rl algorithm, and should have running game behind


pygame.init()


# Screen dimensions and settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 40  # Each cell of the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Maze dimensions
ROWS = len(maze)
COLS = len(maze[0])


player_pos = [1, 1]  # Start at maze[1][1]
goal_pos = [11, 13]  # Set the goal at maze[11][13]

def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw the player
def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw the goal
def draw_goal():
    pygame.draw.rect(screen, RED, (goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))



def move_player(dx, dy):
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    # Check if new position is within bounds and not a wall
    if 0 <= new_x < ROWS and 0 <= new_y < COLS and maze[new_x][new_y] == 0:
        player_pos[0], player_pos[1] = new_x, new_y

action_map = {
    1: (-1, 0),
    2: (1, 0),
    3: (0, -1),
    4: (0, 1)
}

def take_action():
    action_x, action_y = action_map[random.randint(1,4)]

    move_player(action_x, action_y)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    draw_maze()
    draw_player()
    draw_goal()

    take_action()
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(-1, 0)
            elif event.key == pygame.K_DOWN:
                move_player(1, 0)
            elif event.key == pygame.K_LEFT:
                move_player(0, -1)
            elif event.key == pygame.K_RIGHT:
                move_player(0, 1)
    """

    # Check for win condition
    if player_pos == goal_pos:
        print("You reached the goal!")
        running = False

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()


pygame.quit()
