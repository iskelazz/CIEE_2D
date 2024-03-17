# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *

from config import GRAPHICS_DIR


# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}
            
    @classmethod
    def CargarImagen(cls, name, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if name in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join(GRAPHICS_DIR, name)
            try:
                imagen = pygame.image.load(fullname)
            except (pygame.error):
                raise (SystemExit)
            imagen = imagen.convert()
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[name] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, name):
        # Si el nombre de archivo está entre los recursos ya cargados
        if name in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(GRAPHICS_DIR, name)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[name] = datos
            # Se devuelve
            return datos
