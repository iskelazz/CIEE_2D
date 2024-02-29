class Tile:
    def __init__(self, sprite, passable):
        self.sprite = sprite
        self.passable = passable  # Determina si los objetos pueden pasar por encima del tile

    def draw(self, screen, position):
        if self.sprite:
            screen.blit(self.sprite, position)
