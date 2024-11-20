import pygame
from typing import Optional
from pygame import Surface
import random
import sys

class MazeGame:
    NAME: str = "Maze Game"
    
    # Parameters
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600
    CELL_SIZE: int = 40
    
    # Constants
    WHITE: tuple = (255, 255, 255)
    BLACK: tuple = (0, 0, 0)
    GREEN: tuple = (0, 255, 0)
    RED: tuple = (255, 0, 0)
    
    # Maze dimensions
    ROWS: int = 0
    COLS: int = 0
    
    
    # Variables
    screen: Surface = None
    player_position:list  = None
    goal_position: list = None
    maze: list = None
    
    action_map: dict = {
        1: (-1, 0),
        2: (1, 0),
        3: (0, -1),
        4: (0, 1)
    }
    
    
    def __init__(self, name:str) -> None:
        self.NAME=name
        pygame.init()
      
      
    def prepare_environment(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.NAME)
        
    
    def configure_maze(
        self, 
        maze:list=None, 
        player_pos:list=None, 
        goal_pos:list=None
    )  -> None:
        
        self.maze=maze if maze else None
        self.player_position=player_pos if player_pos else None
        self.goal_position=goal_pos if goal_pos else None
         
        
            
        
    
    def draw_maze(self) -> list:
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = self.BLACK if self.maze[row][col] == 1 else self.WHITE
                pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
       
        self.ROWS = len(self.maze)
        self.COLS = len(self.maze[0])

    # Draw the player
    def draw_player(self):
        pygame.draw.rect(
            self.screen, 
            self.GREEN, 
            (
                self.player_position[1] * self.CELL_SIZE, 
                self.player_position[0] * self.CELL_SIZE, 
                self.CELL_SIZE, 
                self.CELL_SIZE
            )
        )

    # Draw the goal
    def draw_goal(self):
        pygame.draw.rect(
            self.screen, 
            self.RED, 
            (
                self.goal_position[1] * self.CELL_SIZE, 
                self.goal_position[0] * self.CELL_SIZE, 
                self.CELL_SIZE, 
                self.CELL_SIZE
            )
        )

    def move_player(self, dx, dy):
        new_x, new_y = self.player_position[0] + dx, self.player_position[1] + dy
        # Check if new position is within bounds and not a wall
        if 0 <= new_x < self.ROWS and 0 <= new_y < self.COLS and self.maze[new_x][new_y] == 0:
            self.player_position[0], self.player_position[1] = new_x, new_y

    def take_random_action(self):
        action_x, action_y = self.action_map[random.randint(1,4)]

        self.move_player(action_x, action_y)

        
    
    
    
    def game_loop(self):
        # Main game loop
        running = True
        while running:
            self.prepare_environment()
            self.screen.fill(self.WHITE)
            self.draw_maze()
            self.draw_player()
            self.draw_goal()

            # self.take_random_action()
            # Intentional Action
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_player(1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_player(0, 1)
            

            # Check for win condition
            if self.player_position == self.goal_position:
                print("You reached the goal!")
                running = False

            # Clear the screen
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        pygame.quit()
        sys.exit()
        
        pygame.quit()