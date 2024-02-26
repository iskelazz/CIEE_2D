class Utils:
    @staticmethod
    def draw_text_with_shadow(screen, text, position, font, color=(255, 255, 255), shadow_color=(0, 0, 0), shadow_offset=2):
        """Dibuja texto con efecto de sombra en la pantalla."""
        # Posición de la sombra
        shadow_position = (position[0] + shadow_offset, position[1] + shadow_offset)
        # Superficie de la sombra
        text_shadow = font.render(text, True, shadow_color)
        shadow_rect = text_shadow.get_rect(center=shadow_position)
        screen.blit(text_shadow, shadow_rect)
        
        # Superficie del texto principal
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)