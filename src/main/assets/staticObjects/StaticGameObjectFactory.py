from assets.staticObjects.Fence import Fence
from assets.staticObjects.HoleStatic import HoleStatic
from assets.staticObjects.Pit import Pit
class StaticObjectFactory:
    
    @staticmethod
    def create_object(obj_type, sprite, position):
        # Diccionario que mapea tipos de objeto a sus clases constructoras
        obj_class_map = {
            "Fence": Fence,
            "Hole":HoleStatic,
            "Pit":Pit,
            # Añadir mas mapeos
        }

        if obj_type in obj_class_map:
            return obj_class_map[obj_type](sprite, position)
        else:
            raise ValueError(f"Unknown object type: {obj_type}")