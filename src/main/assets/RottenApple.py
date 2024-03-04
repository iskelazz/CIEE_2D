import os
from config import GRAPHICS_DIR
from assets.Consumable import Consumable 

class RottenApple(Consumable):
    def __init__(self, staticPositions):
        super().__init__(os.path.join(GRAPHICS_DIR, 'apple_rotten.png'), staticPositions)

