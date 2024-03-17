import pygame
from config import Config 

class Area:
    def __init__(self, tag, x, y, width, height):
        self.tag = tag
        self.rect = pygame.Rect(x*Config.CELL_SIZE, y*Config.CELL_SIZE, width*Config.CELL_SIZE, height*Config.CELL_SIZE)