import json
import os
import pygame
from config import Config 
from phases.Tile import Tile  
from assets.staticObjects.StaticGameObjectFactory import StaticObjectFactory

class LevelManager:
    def __init__(self, screen):
        self.screen = screen
        self.cell_number_x = 0  
        self.cell_number_y = 0
        self.cell_size = Config.CELL_SIZE
        self.layers = []  
        self.sprite_groups = {}

    def load_sprites(self, sprites_data):
        sprites_dict = {}
        for key, sprite_info in sprites_data.items():
            if isinstance(sprite_info, list):  # Si hay información de recorte (y posiblemente rotación)
                sprite_path = os.path.join(Config.GRAPHICS_DIR, sprite_info[0])
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
                sprite_path = os.path.join(Config.GRAPHICS_DIR, sprite_info)
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
            # Establece el tamaño de la fase en casillas
            self.cell_number_x = len(data['layers'][0]['tiles'][0])  
            self.cell_number_y = len(data['layers'][0]['tiles'])

            Config.update_map_size(self.cell_number_x * self.cell_size, self.cell_number_y * self.cell_size)

            for layer_data in data['layers']:
                self.load_layer(layer_data)
            for obj_data in data["objects"]:
                self.load_object(obj_data)


    def draw_level(self,screen, camera_offset):
        """Dibuja todas las capas del nivel."""
        for layer in self.layers:
            for row_idx, row in enumerate(layer):
                for col_idx, tile in enumerate(row):
                    if tile:
                        # Aplica el desplazamiento de la cámara aquí
                        tile_position = (col_idx * Config.CELL_SIZE - camera_offset.x, row_idx * Config.CELL_SIZE - camera_offset.y)
                        tile.draw(screen, tile_position)

    def update(self):
        """Actualiza el nivel dibujando todas las capas."""
        self.draw_level()

    
    def load_object(self, obj_data):
        sprite_path = os.path.join(Config.GRAPHICS_DIR, obj_data["sprite"])
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
            if obj_data["type"] not in self.sprite_groups:
                self.sprite_groups[obj_data["type"]] = pygame.sprite.Group()
            self.sprite_groups[obj_data["type"]].add(obj)

    #Funcion para pintar en pantalla todos los objetos estaticos
    def draw_objects(self, screen, camera_offset):
        for group in self.sprite_groups.values():
            for obj in group:
                # Calcula la nueva posición del objeto basada en el desplazamiento de la cámara
                obj_position = (obj.rect.x - camera_offset.x, obj.rect.y - camera_offset.y)
                screen.blit(obj.image, obj_position)

    #Esta funcion verifica las colisiones del jugador con los objetos estaticos y las gestiona
    def check_collisions(self, snake, manager, explosion):
        head = snake.segments.sprites()[0]
        full_body_collide = False
        for group in self.sprite_groups.values():
            collided_sprites = pygame.sprite.spritecollide(head, group, False)
            collisions = pygame.sprite.groupcollide(snake.segments, group, False, False)
            if len(collisions) == len(snake.segments):
                full_body_collide = True
            for sprite in collided_sprites:
                sprite.handle_collision(manager,full_body_collide,snake.state,explosion)

    #Calculamos las posiciones de los objetos estaticos para evitar la aparicion de objetos aleatorios en esas posiciones
    def precalculate_static_objects_positions(self):
        occupied_positions = set()
        for group in self.sprite_groups.values():
            for obj in group:
                # Asume que cada objeto tiene un método occupied_positions() que devuelve las posiciones que ocupa.
                occupied_positions.add(tuple(obj.occupied_positions()))
        return occupied_positions
