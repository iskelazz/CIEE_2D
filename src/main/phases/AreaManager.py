from config import Config

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

"Se encarga de facilitar metodos para comprobar que objetos se encuentran en determinadas areas en las que se subdividen las fases"
class AreaManager(metaclass=SingletonMeta):
    def __init__(self):
        self.areas = {}  # Inicializa sin áreas

    def load_areas(self, new_areas):
        self.areas = new_areas  # Carga o sustituye las áreas

    def get_area_tag_by_point(self, x, y):
        """Indica en que area se encuentra el punto, None si no esta en ninguna"""
        for tag, area in self.areas.items():
            if area.rect.collidepoint(x, y):
                return tag
        return None

    def get_area_tag_by_object(self, obj):
        """Indica en que area se encuentra el objeto, None si no esta en ninguna"""
        for tag, area in self.areas.items():
            if area.rect.colliderect(obj.rect):
                return tag
        return None

    def count_objects_in_area(self, objects, area_tag):
        """Cuenta cuantos objetos de un grupo pasado por parametro hay en un area pasada por parametro"""
        count = 0
        area = self.areas.get(area_tag)
        if not area:
            return count  # Área no encontrada
        for obj in objects:
            if area.rect.colliderect(obj.rect):
                count += 1
        return count

    def coords(self, area_tag):
        """Recuperamos las coordenadas de un area pasada con tag por parametro"""
        area = self.areas.get(area_tag)
        if area:
            return [area.rect.x // Config.CELL_SIZE, area.rect.y // Config.CELL_SIZE, area.rect.width // Config.CELL_SIZE, area.rect.height // Config.CELL_SIZE]
        return None

    @staticmethod
    def get_instance():
        """Proporciona acceso a la instancia única de AreaManager."""
        return AreaManager()