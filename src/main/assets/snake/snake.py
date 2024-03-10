import pygame
import os
import time
from assets.snake.normalState import NormalState
from assets.snake.pacmanState import PacmanState
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from config import GRAPHICS_DIR, CELL_SIZE


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
    def __init__(self):
        self.load_images()
        self.segments = Group()
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.create_snake()
        self.last_update_time = time.time()
        self.state = NormalState(self)
        self.speed = 9 # 9 movimientos por segundo
        self.draw_segments = self.draw_snake_segments

    def set_state(self, new_state_cls):
        self.state.on_exit()  # Llama a on_exit del estado actual
        self.state = new_state_cls # Crea una nueva instancia del nuevo estado
        self.state.on_enter()

    def load_images(self):
        # Convertimos los Vector2 a tuplas para usarlos como claves
        self.head_images = {
            (0, -1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_up.png')).convert_alpha(),
            (0, 1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_down.png')).convert_alpha(),
            (1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_right.png')).convert_alpha(),
            (-1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_left.png')).convert_alpha(),
        }
        self.tail_images = {
            (0, -1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_up.png')).convert_alpha(),
            (0, 1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_down.png')).convert_alpha(),
            (1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_right.png')).convert_alpha(),
            (-1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_left.png')).convert_alpha(),
        }

        self.body_vertical = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_horizontal.png')).convert_alpha()

        self.body_tr = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_bl.png')).convert_alpha()

        self.head_blink_images = {
            (0, -1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_head_up.png')).convert_alpha(),
            (0, 1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_head_down.png')).convert_alpha(),
            (1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_head_right.png')).convert_alpha(),
            (-1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_head_left.png')).convert_alpha(),
        }

        self.tail_blink_images = {
            (0, -1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_tail_up.png')).convert_alpha(),
            (0, 1): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_tail_down.png')).convert_alpha(),
            (1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_tail_right.png')).convert_alpha(),
            (-1, 0): pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_tail_left.png')).convert_alpha(),
        }
        # Suponiendo que tienes sprites de parpadeo para el cuerpo
        self.body_vertical_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_vertical.png')).convert_alpha()
        self.body_horizontal_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_horizontal.png')).convert_alpha()

        self.body_tr_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_tr.png')).convert_alpha()
        self.body_tl_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_tl.png')).convert_alpha()
        self.body_br_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_br.png')).convert_alpha()
        self.body_bl_blink = pygame.image.load(os.path.join(GRAPHICS_DIR, 'white_body_bl.png')).convert_alpha()

    # Asegúrate de convertir los Vector2 a tuplas cuando accedas a las imágenes
    def draw_snake_segments(self):
        for index, segment in enumerate(self.segments):
            position = self.body[index]
            segment.update(position)
            if index == 0:
                # Convertimos self.direction a tupla antes de usarlo
                segment.image = self.head_images[tuple(self.direction)]
            elif index == len(self.body) - 1:
                direction = self.body[-1] - self.body[-2]
                # Convertimos la dirección a tupla antes de usarla
                segment.image = self.tail_images[tuple(direction)]
            else:
                # Determina la orientación y los giros para los segmentos del cuerpo
                prev_segment = self.body[index - 1]
                next_segment = self.body[index + 1]
                if prev_segment.x == next_segment.x:
                    segment.image = self.body_vertical
                elif prev_segment.y == next_segment.y:
                    segment.image = self.body_horizontal
                else:
                    # Aquí determinamos los giros
                    if prev_segment.x < position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x < position.x:
                        segment.image = self.body_tl
                    elif prev_segment.x > position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x > position.x:
                        segment.image = self.body_tr
                    elif prev_segment.x < position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x < position.x:
                        segment.image = self.body_bl
                    elif prev_segment.x > position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x > position.x:
                        segment.image = self.body_br

    def create_snake(self):
        "Creación y pintado inicial de la serpiente, siempre se crea en horizontal"
        for index, position in enumerate(self.body):
            if index == 0:
                segment = SnakeSegment(position,index, 'head')
                # Aquí convertimos self.direction a tupla
                segment.image = self.head_images[tuple(self.direction)]
            elif index == len(self.body) - 1:
                segment = SnakeSegment(position,index, 'tail')
                # Aquí convertimos la dirección de la cola a tupla
                direction = self.body[-1] - self.body[-2]
                segment.image = self.tail_images[tuple(direction)]
            else:
                segment = SnakeSegment(position,index)
                segment.image = self.body_horizontal
            self.segments.add(segment)

    def update(self, current_time):
        self.state.update()  # Asegúrate de que el estado actual se actualice
        if current_time - self.last_update_time > 1/self.speed:
            if self.new_block:
                self.grow()
                self.new_block = False
            if self.direction != Vector2(0, 0):
                new_body = self.body[:-1]
                new_body.insert(0, new_body[0] + self.direction)
                self.body = new_body
                self.draw_segments()  # Utiliza el método de dibujo actual
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
