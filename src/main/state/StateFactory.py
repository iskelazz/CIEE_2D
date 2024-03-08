from state.StartScreenState import StartScreenState
from state.PlayingState1 import PlayingState1 
from state.PlayingState2 import PlayingState2 
from state.PlayingState3 import PlayingState3 
from state.FinalScreenState import FinalScreenState 
from state.PauseState import PauseState
from state.MenuState import MenuState 
from state.GameOverState import GameOverState


class StateFactory:
    @staticmethod
    def create_state(state_id, game):
        if state_id == 'START':
            return StartScreenState(game)
        elif state_id == 'PLAYING1':
            return PlayingState1(game)
        elif state_id == 'PLAYING2':
            return PlayingState2(game)
        elif state_id == 'PLAYING3':
            return PlayingState3(game)
        elif state_id == 'PAUSE':
            return PauseState(game)
        elif state_id == 'FINAL_SCREEN':
            return FinalScreenState(game)
        elif state_id == 'MENU':
            return MenuState(game)
        elif state_id == 'GAME_OVER':
            return GameOverState(game)
        else:
            raise ValueError(f"Unknown state ID: {state_id}")