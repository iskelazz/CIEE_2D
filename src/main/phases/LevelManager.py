import json
import os
import pygame
from config import GRAPHICS_DIR  
from phases.Tile import Tile  
from assets.staticObjects.StaticGameObjectFactory import StaticObjectFactory

class LevelManager:
    def __init__(self, screen, cell_size, cell_number):
        self.screen = screen
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.layers = []  
        self.objects = []
        self.sprite_groups = {}

    def load_sprites(self, sprites_data):
        sprites_dict = {}
        for key, sprite_info in sprites_data.items():
            if isinstance(sprite_info, list):  # Si hay información de recorte (y posiblemente rotación)
                sprite_path = os.path.join(GRAPHICS_DIR, sprite_info[0])
                x, y, width, height = sprite_info[1:5]
                # Comprueba si hay un valor de rotación; de lo contrario, usa 0
                rotation = sprite_info[5] if len(sprite_info) > 5 else 0
                
                full_sprite = pygame.image.load(sprite_path).convert_alpha()
                cropped_sprite = full_sprite.subsurface((x, y, width, height))
                # Aplica rotación solo si es necesario
                if rotation != 0:
                    sprite = pygame.transform.rotate(cropped_sprite, rotation)
                else:
                    sprite = cropped_sprite  # No se aplica rotación
                sprites_dict[key] = sprite
            else:  # Carga la imagen completa si no hay recorte ni rotación
                sprite_path = os.path.join(GRAPHICS_DIR, sprite_info)
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprites_dict[key] = sprite
        return sprites_dict


    def load_layer(self, layer_data):
        """Carga una capa individual desde los datos proporcionados."""
        sprites_dict = self.load_sprites(layer_data['sprites'])
        layer_tiles = [
            [Tile(sprites_dict[str(tile_type)], True) if tile_type and str(tile_type) in sprites_dict else None
             for tile_type in row] for row in layer_data['tiles']
        ]
        self.layers.append(layer_tiles)

    def load_level_from_json(self, json_path):
        """Carga el nivel y sus capas desde un archivo JSON."""
        with open(json_path) as f:
            data = json.load(f)
            for layer_data in data['layers']:
                self.load_layer(layer_data)
            for obj_data in data["objects"]:
                self.load_object(obj_data)

    def draw_level(self):
        """Dibuja todas las capas del nivel."""
        for layer in self.layers:
            for row_idx, row in enumerate(layer):
                for col_idx, tile in enumerate(row):
                    if tile:
                        tile_position = (col_idx * self.cell_size, row_idx * self.cell_size)
                        tile.draw(self.screen, tile_position)

    def update(self):
        """Actualiza el nivel dibujando todas las capas."""
        self.draw_level()

    
    def load_object(self, obj_data):
        sprite_path = os.path.join(GRAPHICS_DIR, obj_data["sprite"])
        full_sprite = pygame.image.load(sprite_path).convert_alpha()

        # Aplicar recorte si es necesario
        if "crop" in obj_data:
            x, y, width, height = obj_data["crop"]
            sprite = full_sprite.subsurface((x, y, width, height))
        else:
            sprite = full_sprite

        # Aplicar rotación si es necesario
        if obj_data.get("rotation", 0) != 0:
            sprite = pygame.transform.rotate(sprite, obj_data["rotation"])

        for position in obj_data["positions"]:
            obj = StaticObjectFactory.create_object(obj_data["type"], sprite, position)

            # Añadir el objeto a la lista general y al grupo de sprites correspondiente
            self.objects.append(obj)
            if obj_data["type"] not in self.sprite_groups:
                self.sprite_groups[obj_data["type"]] = pygame.sprite.Group()
            self.sprite_groups[obj_data["type"]].add(obj)

    #Funcion para pintar en pantalla todos los objetos estaticos
    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.screen)

    #Esta funcion verifica las colisiones del jugador con los objetos estaticos y las gestiona
    def check_collisions(self, head, manager):
        for group in self.sprite_groups.values():
            collided_sprites = pygame.sprite.spritecollide(head, group, False)
            for sprite in collided_sprites:
                sprite.handle_collision(manager)

    #Calculamos las posiciones de los objetos estaticos para evitar la aparicion de objetos aleatorios en esas posiciones
    def precalculate_static_objects_positions(self):
        occupied_positions = set()
        for obj in self.objects:
            occupied_positions.add(tuple (obj.occupied_positions()))
        return occupied_positions
