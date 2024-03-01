import os

# Define la base de las rutas de los recursos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Esto te llevará al directorio raíz del proyecto
GRAPHICS_DIR = os.path.join(BASE_DIR, 'main' , 'resources', 'graphics')
FONTS_DIR = os.path.join(BASE_DIR, 'main' , 'resources', 'fonts')
LEVEL_DIR = os.path.join(BASE_DIR, 'main' , 'phases')
SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 800
CELL_SIZE = 40