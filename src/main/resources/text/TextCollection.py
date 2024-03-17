class TextColection:
    
    @staticmethod
    def get_pause_text():
        return 'PAUSA'

    @staticmethod
    def get_menu_options_text():
        return ['JUGAR', 'SALIR']

    @staticmethod
    def get_story_1_text():
        return ['En un pacífico y exuberante bosque mágico...',
                    'la armonía se ve interrumpida por un malvado águila...',
                    'que ha robado los preciados huevos de una madre serpiente...',
                    'La valiente serpiente se embarca en una peligrosa misión...',
                    'para demostrar su valentía y recuperar lo que le pertenece...',
                    '¿Estás listo?']
    @staticmethod
    def get_story_2_text():
        return ['La serpiente se encuentra frente a un río peligroso...',
                    'nuevos enemigos se cruzan en su camino...',
                    'buscan poner fin a la mision de recuperar los huevos robados...',
                    '¿Podrá la serpiente derrotarlos y superar las trampas?']
    
    @staticmethod
    def get_story_3_text():
        return ['Finalmente, la serpiente ha llegado a la guarida del águila...',
                    'Pero el verdadero desafío aguarda en la cima...',
                    'solo con coraje, habilidad y determinación podrá vencerla...',
                    '¿Recuperará sus huevos, restaurando así la paz en el bosque?']
    
    @staticmethod
    def get_story_4_text():
        return ['Y así fué como la valiente serpiente derrotó al águila...',
                    'Consiguió restaurar la paz en el bosque...',
                    'sus habitantes se lo agradecieron con miles de ofrendas...',
                    'Y demostró que con valentía se puede lograr todo.']


    @staticmethod
    def get_gameover_retry_text():
        return 'Presiona ENTER para reintentar'
    
    @staticmethod
    def get_gameover_exit_text():
        return 'Presiona ESC para Menú'
    @staticmethod
    def get_gameover_score_text():
        return 'Puntuación: '
    @staticmethod
    def get_gameover_text():
        return 'GAME OVER'
