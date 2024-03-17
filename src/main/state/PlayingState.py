import pygame
from abc import ABC, abstractmethod
from state.GameState import GameState
from phases.AreaManager import AreaManager
from phases.LevelManager import LevelManager
import os
from config import Config
import time
import random
from assets.rottenApple import RottenApple
from assets.snake.snake import Snake

class PlayingState(GameState, ABC):
    def __init__(self, game):
        super().__init__(game)

        #inicializacion de score
        self.game.score.init_level_score()

        #Definimos grupos de la fruta aleatoria
        self.apple_group = pygame.sprite.Group() 
        self.rotten_apple_group = pygame.sprite.Group()  
        self.explosions_group = pygame.sprite.Group()

        self.activated_areas = {}  # Diccionario para manejar el estado por área
        self.completed_areas = set()  # Para registrar áreas que ya completaron la generación

        self.snake = None  

    def initialize_snake(self, position):
        """Método para inicializar la serpiente. Las clases hijas llamarán a este método con sus propias posiciones."""
        self.snake = Snake(position[0], position[1])

    def fruit_sorting(self, area, number, fruit_class):
        "Llama a la función para añadir manzanas tantas veces como este definido en inicializar_apples"
        for _ in range(number):  # Generar "number" manzanas por área
                self.add_apple_in_area(area, fruit_class)

    def add_apple_in_area(self, area, fruit_class):
        "Crea la manzana de la clase pasada por parametro y la añade al grupo de manzanas"
        apple = fruit_class(lambda: self.level_manager.precalculate_static_objects_positions())
        apple.randomize(self.snake.body, area)
        self.apple_group.add(apple)

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Dibuja todos los elementos del juego en la pantalla."""
        pass
        
    def handle_events(self, events):
        #Metodo que se encarga de reaccionar a los inputs del jugador
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.screen_manager.push_state('PAUSE')
                else:
                    # Actualiza la dirección basada en la tecla presionada
                    self.snake.update_direction(event.key)

    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(Config.LEVEL_DIR, json_path))
    
    @abstractmethod
    def check_collisions(self):
        """Verifica y maneja las colisiones."""
        pass
    
    @abstractmethod
    def tag(self):
        pass

    @abstractmethod
    def next_level(self):
        pass

    def respawn_object_if_missing(self, object, group, timer, interval):
        """
        Comprueba si un objeto está en un grupo y, si no está, activa un timer.
        Si el timer supera el intervalo especificado, vuelve a añadir el objeto al grupo.

        :param object: El objeto a comprobar y potencialmente reaparecer.
        :param group: El grupo de sprites al que pertenece el objeto.
        :param timer: El temporizador actual para el objeto. None si el objeto no está en cooldown.
        :param interval: El intervalo de tiempo (en milisegundos) para reaparecer el objeto.
        :return: El estado actualizado del temporizador para el objeto.
        """
        current_time = pygame.time.get_ticks()  # Obtiene el tiempo actual
        if object not in group:
            if timer is None:
                timer = current_time
            elif current_time - timer > interval:
                group.add(object)
                timer = None
        else:
            timer = None  # Resetea el timer si el objeto ya está en el grupo
        
        return timer

    def check_area_activation(self, current_time):
        area_tag = AreaManager.get_instance().get_area_tag_by_point(
            self.snake.segments.sprites()[0].rect.centerx,
            self.snake.segments.sprites()[0].rect.centery
        )
        if area_tag and area_tag not in self.completed_areas:
            self.activate_rotten_apples_generation(area_tag)

    def activate_rotten_apples_generation(self, area_tag):
        if area_tag not in self.activated_areas:
            self.activated_areas[area_tag] = {
                "last_generation_time": time.time(),
                "to_generate": random.randint(1, 3),
                "generated": 0
            }

    def generate_rotten_apple(self, current_time):
        for area_tag, state in list(self.activated_areas.items()):
            if state["generated"] < state["to_generate"]:
                if current_time - state["last_generation_time"] >= 5:
                    area = AreaManager.get_instance().coords(area_tag)
                    self.add_apple_in_area(area, RottenApple)
                    state["last_generation_time"] = current_time
                    state["generated"] += 1
                    if state["generated"] >= state["to_generate"]:
                        # Si se ha alcanzado el número de generaciones para esta área, la elimina
                        del self.activated_areas[area_tag]
                        self.completed_areas.add(area_tag)