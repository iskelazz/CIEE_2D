import pygame

cell_size = 40
cell_number = 20

#Esta clase se encarga de pintar el transfondo de la fase
class GameBoard:
    def __init__(self, screen, cell_size, cell_number):
        self.screen = screen
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.grass_color = (167, 209, 61)  # Color del pasto

    def draw_grass(self):
        """Pinta pasto de fondo"""
        grass_color = (167,209,61)
        for row in range(self.cell_number):
            if row % 2 == 0: 
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size,row * self.cell_size,self.cell_size,self.cell_size)
                        pygame.draw.rect(self.screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size,row * self.cell_size,self.cell_size,self.cell_size)
                        pygame.draw.rect(self.screen,grass_color,grass_rect)	


    def update(self):
        """Actualiza y dibuja los elementos del tablero de juego."""
        self.draw_grass()