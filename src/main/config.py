import os

class Config:
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            cls.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Esto te llevará al directorio raíz del proyecto
            cls.GRAPHICS_DIR = os.path.join(cls.BASE_DIR, 'main', 'resources', 'graphics')
            cls.SOUNDS_DIR = os.path.join(cls.BASE_DIR, 'main', 'resources', 'sounds')
            cls.FONTS_DIR = os.path.join(cls.BASE_DIR, 'main', 'resources', 'fonts')
            cls.LEVEL_DIR = os.path.join(cls.BASE_DIR, 'main', 'phases')
            cls.SCREEN_WIDTH = 800  
            cls.SCREEN_HEIGHT = 800
            cls.CELL_SIZE = 40
            # Variables dinámicas
            cls.map_size = None  # Será actualizado con el tamaño del mapa
            cls._initialized = True

    @classmethod
    def update_map_size(cls, width, height):
        cls.map_size = (width, height)
