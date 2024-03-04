import os
from config import GRAPHICS_DIR
from assets.Consumable import Consumable  # Asegúrate de importar la nueva clase padre

class RedApple(Consumable):
    def __init__(self, staticPositions):
        super().__init__(os.path.join(GRAPHICS_DIR, 'apple.png'), staticPositions)

