from assets import redapple

class FruitFactory:
    def create_fruit(x, y, fruit_type):
        if fruit_type == "RedApple":
            return redapple(x, y)
        else:
            return None  # Manejo de un tipo de fruta desconocido o error