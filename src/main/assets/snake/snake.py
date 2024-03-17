import pygame
import os
import time
from assets.snake.normalState import NormalState
from assets.snake.pacmanState import PacmanState
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from config import GRAPHICS_DIR, CELL_SIZE, SOUNDS_DIR


class SnakeSegment(Sprite):
    def __init__(self, position, number,segment_type='body'):
        super().__init__()
        self.number=number
        self.position = position
        self.segment_type = segment_type
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(pygame.Color('white'))  # Color por defecto para el cuerpo
        self.rect = self.image.get_rect(topleft=(position.x * CELL_SIZE, position.y * CELL_SIZE))
    def update(self, position):
        self.rect.topleft = (position.x * CELL_SIZE, position.y * CELL_SIZE)

class Snake:
    def __init__(self, pos_x, pos_y):
        self.load_images()
        self.segments = Group()
        
        self.retrieved_eggs=0
        #Posicion del cuerpo, la pasada por parametro es la cabeza, se situa siempre en horizontal mirando a la derecha
        self.body = [Vector2(pos_x, pos_y), Vector2(pos_x-1, pos_y), Vector2(pos_x-2, pos_y)]
        self.direction = Vector2(1, 0)
        self.new_direction = Vector2(1, 0)
        self.new_block = False
        
        #La imagen que muestra es la de la serpiente en estado normal, puede cambiar para parpadear en estados alterados de la serpietne
        self.mode_image = "normal"
        self.create_snake()
        self.last_update_time = time.time()
        self.state = NormalState(self)
        self.speed = 7 # 7 movimientos por segundo

        #sonidos
        self.red_apple_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'eat_red_apple.wav'))
        self.rotten_apple_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'eat_rotten_apple.wav'))
        self.bat_hit_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'enemy_bat_hit.wav'))
        self.bat_kill_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'enemy_kill.wav'))
        self.wooden_trap_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'wooden_trap.wav'))
        
    def set_state(self, new_state_cls):
        self.state.on_exit()  # Llama a on_exit del estado actual
        self.state = new_state_cls # Crea una nueva instancia del nuevo estado
        self.state.on_enter()

    def load_images(self):
        modes = ["normal", "white", "yellow"]
        directions = {
            (0, -1): "up",
            (0, 1): "down",
            (1, 0): "right",
            (-1, 0): "left",
        }

        self.images = {mode: {"head": {}, "tail": {}, "body_vertical": None, "body_horizontal": None, "body_tr": None, "body_tl": None, "body_br": None, "body_bl": None} for mode in modes}

        for mode in modes:
            for direction, dir_name in directions.items():
                self.images[mode]["head"][direction] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/head_{dir_name}.png")).convert_alpha()
                self.images[mode]["tail"][direction] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/tail_{dir_name}.png")).convert_alpha()

            self.images[mode]["body_vertical"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_vertical.png")).convert_alpha()
            self.images[mode]["body_horizontal"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_horizontal.png")).convert_alpha()
            self.images[mode]["body_tr"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_tr.png")).convert_alpha()
            self.images[mode]["body_tl"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_tl.png")).convert_alpha()
            self.images[mode]["body_br"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_br.png")).convert_alpha()
            self.images[mode]["body_bl"] = pygame.image.load(os.path.join(GRAPHICS_DIR, f"{mode}_snake/body_bl.png")).convert_alpha()



    # Asegúrate de convertir los Vector2 a tuplas cuando accedas a las imágenes
    def draw_snake_segments(self):
        for index, segment in enumerate(self.segments):
            position = self.body[index]
            segment.update(position)
            if index == 0:
                # Convertimos self.direction a tupla antes de usarlo
                segment.image = self.images[self.mode_image]["head"][tuple(self.direction)]
            elif index == len(self.body) - 1:
                direction = self.body[-1] - self.body[-2]
                # Convertimos la dirección a tupla antes de usarla
                segment.image = self.images[self.mode_image]["tail"][tuple(direction)]
            else:
                # Determina la orientación y los giros para los segmentos del cuerpo
                prev_segment = self.body[index - 1]
                next_segment = self.body[index + 1]
                if prev_segment.x == next_segment.x:
                    segment.image = self.images[self.mode_image]["body_vertical"]
                elif prev_segment.y == next_segment.y:
                    segment.image = self.images[self.mode_image]["body_horizontal"]
                else:
                    # Aquí determinamos los giros
                    if prev_segment.x < position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x < position.x:
                        segment.image = self.images[self.mode_image]["body_tl"]
                    elif prev_segment.x > position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x > position.x:
                        segment.image = self.images[self.mode_image]["body_tr"]
                    elif prev_segment.x < position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x < position.x:
                        segment.image = self.images[self.mode_image]["body_bl"]
                    elif prev_segment.x > position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x > position.x:
                        segment.image = self.images[self.mode_image]["body_br"]

    def create_snake(self):
        "Creación y pintado inicial de la serpiente, siempre se crea en horizontal"
        for index, position in enumerate(self.body):
            if index == 0:
                segment = SnakeSegment(position,index, 'head')
                # Aquí convertimos self.direction a tupla
                segment.image = self.images[self.mode_image]["head"][tuple(self.direction)]
            elif index == len(self.body) - 1:
                segment = SnakeSegment(position,index, 'tail')
                # Aquí convertimos la dirección de la cola a tupla
                direction = self.body[-1] - self.body[-2]
                segment.image = self.images[self.mode_image]["tail"][tuple(direction)]
            else:
                segment = SnakeSegment(position,index)
                segment.image = self.images[self.mode_image]["body_horizontal"]
            self.segments.add(segment)

    def update(self, current_time):
        self.state.update()  # Asegúrate de que el estado actual se actualice
        if current_time - self.last_update_time > 1/self.speed:
            self.direction = self.new_direction
            if self.new_block:
                self.grow()
                self.new_block = False
            if self.direction != Vector2(0, 0):
                new_body = self.body[:-1]
                new_body.insert(0, new_body[0] + self.direction)
                self.body = new_body
                self.draw_snake_segments()  # Utiliza el método de dibujo actual
            self.last_update_time = current_time


    def grow(self):
        # Calcula la nueva posición para el segmento basándose en la dirección de crecimiento.
        tail = self.body[-1]
        tail_direction = self.body[-1] - self.body[-2] if len(self.body) > 1 else self.direction
        new_segment_position = tail - tail_direction  # Añade en dirección opuesta a su movimiento.
        self.body.append(new_segment_position)

        # Crea y añade el nuevo segmento al grupo de sprites.
        new_segment = SnakeSegment(new_segment_position, self.segments.__len__(), 'body')
        self.segments.add(new_segment)

    def add_block(self):
        self.new_block = True

    def is_snake_out_of_bounds(self, cell_number_x, cell_number_y):
    #Comprueba si la serpiente esta en los limites del tablero    
        head = self.body[0]
        return not (0 <= head.x < cell_number_x and 0 <= head.y < cell_number_y)

    def handle_input(self, event):
        self.state.handle_input(event)
    
    def reduce_body(self):
        if len(self.body) > 1:
            # Eliminamos el último elemento del cuerpo de la serpiente
            self.body.pop()
            # Eliminamos también el último segmento del grupo de sprites
            self.segments.remove(self.segments.sprites()[-1])

    def update_direction(self, key):
        """Actualiza la dirección de la serpiente basada en la entrada del usuario."""
        directions = {
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1),
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
        }
        if key in directions and directions[key] != -self.direction:
            self.new_direction = directions[key]
