from state.StateFactory import StateFactory

class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None
        self.previous_state = None

    def change_state(self, state_id):
        if state_id not in self.states:
            self.states[state_id] = StateFactory.create_state(state_id, self.game)
        self.previous_state = self.current_state  # Guardar el estado actual como anterior antes de cambiar
        self.current_state = self.states[state_id]

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

    def return_to_previous_state(self):
        if self.previous_state:
            self.current_state = self.previous_state
            self.previous_state = None 