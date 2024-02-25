from phases.screen1fruits import Screen1fruits

class Phase1:
    def __init__(self, width, height):
        self.screens = {
            1: Screen1fruits(width, height),
        }

    def update(self, screen_number):
        self.screens[screen_number].update()

    def render(self, screen, screen_number):
        self.screens[screen_number].render(screen)
