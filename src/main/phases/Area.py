import pygame
from config import CELL_SIZE 

class Area:
    def __init__(self, tag, x, y, width, height):
        self.tag = tag
        self.rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, width*CELL_SIZE, height*CELL_SIZE)