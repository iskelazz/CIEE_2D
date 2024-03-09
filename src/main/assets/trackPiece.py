import pygame, os
from pygame.sprite import Group, Sprite
from pygame.math import Vector2
from config import GRAPHICS_DIR

cell_size = 40
cell_number = 20


class TrackPiece(Sprite):
    def __init__(self, position, orientation='horizontal', piece = 'first'):
        super().__init__()
        self.orientation = orientation
        self.piece = piece
        self.image = self.load_piece()
        self.rect = self.image.get_rect(topleft=(position.x * cell_size, position.y * cell_size))
        
    def load_piece(self):
        image = None
        if self.piece == 'first':
            image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'saw_track_left_edge.png')).convert_alpha()
        elif self.piece == 'mid':
            image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'saw_track_repeating_center.png')).convert_alpha()
        elif self.piece == 'last':
            image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'saw_track_right_edge.png')).convert_alpha()
        
        image = pygame.transform.scale(image, (cell_size, cell_size))
        
        if self.orientation == 'vertical':
            image = pygame.transform.rotate(image, 270)
        
        return image    

    def create_pieces(x, y, lenght, orientation):
        track_piece = Group()
        for i in range(lenght):
            piece = 'mid'
            if i == 0:
                piece = 'first' 
            if i == lenght-1:
                piece = 'last'
                
            if orientation == 'horizontal':        
                track_piece.add(TrackPiece(Vector2(x+i, y), orientation, piece))    
            elif orientation == 'vertical':    
                track_piece.add(TrackPiece(Vector2(x, y+i), orientation, piece))        

        return track_piece
    
    def draw(self, win, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
        win.blit(self.image, adjusted_position)
        
    def get_position(self):
        return  self.rect.x, self.rect.y
    
    def get_orientation(self):
        return self.orientation
         
        
    