from state.StartScreenState import StartScreenState
from state.PlayingState import PlayingState 
from state.PauseState import PauseState
from state.MenuState import MenuState 
from state.GameOverState import GameOverState


class StateFactory:
    @staticmethod
    def create_state(state_id, game):
        if state_id == 'START':
            return StartScreenState(game)
        elif state_id == 'PLAYING':
            return PlayingState(game)
        elif state_id == 'PAUSE':
            return PauseState(game)
        elif state_id == 'MENU':
            return MenuState(game)
        elif state_id == 'GAME_OVER':
            return GameOverState(game)
        else:
            raise ValueError(f"Unknown state ID: {state_id}")