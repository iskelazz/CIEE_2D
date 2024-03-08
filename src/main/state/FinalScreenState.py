import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.redapple import RedApple
from assets.snake.snake import Snake
from phases.LevelManager import LevelManager
import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class FinalScreenState(GameState):
    def __init__(self, game):
        self.game = game

   
    def handle_events(self, events):
        pass

   
    def update(self):
        pass

    
    def draw(self, screen):
        pass