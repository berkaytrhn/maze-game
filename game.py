import pygame
from typing import Optional
from dataclasses import dataclass, field
from pygame import Surface

@dataclass
class Game:
    # Parameters
    SCREEN_WIDTH: int = field(default=600, init=True)
    SCREEN_HEIGHT: int = field(default=600, init=True)
    CELL_SIZE: int = field(default=40, init=True)
    
    # Constants
    WHITE: tuple = field(default=(255, 255, 255), init=False)
    BLACK: tuple = field(default=(0, 0, 0), init=False)
    GREEN: tuple = field(default=(0, 255, 0), init=False)
    RED: tuple = field(default=(255, 0, 0), init=False)
    
    screen: Surface = field(default=None, init=False)
    
    def __init__(self) -> None:
        pygame.init()
        
    def prepare_environment(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pass
    
    