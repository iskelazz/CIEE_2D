import pygame
import random
import os
from assets.consumable import Consumable 
from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20 #temporal
 
class RedApple(Consumable):
	def __init__(self, staticPositions):
		super().__init__(os.path.join(GRAPHICS_DIR, 'apple.png'), staticPositions)