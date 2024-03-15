class TextColection:
    
    @staticmethod
    def get_pause_text():
        return 'PAUSA'

    @staticmethod
    def get_menu_options_text():
        return ['JUGAR', 'SALIR']

    @staticmethod
    def get_introduction_text():
        return ['En un pacífico y exuberante bosque mágico...',
                            'la armonía se ve interrumpida por un malvado águila...',
                            'que ha robado los preciados huevos de una madre serpiente..',
                            'La valiente serpiente se embarca en una peligrosa misión...',
                            'para demostrar su valentía y recuperar lo que le pertenece...',
                            '¿Estás listo?']

    @staticmethod
    def get_gameover_retry_text():
        return 'Presiona ENTER para reintentar'
    
    @staticmethod
    def get_gameover_exit_text():
        return 'Presiona ESC para Menu'
    @staticmethod
    def get_gameover_score_text():
        return 'Puntuación: '
    @staticmethod
    def get_gameover_text():
        return 'GAME OVER'
