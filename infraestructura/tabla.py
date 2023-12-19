'''
Clase abstracta que sirve de plantilla para todas las clases que representan tablas de la BD
'''

from abc import ABC, abstractmethod

class Tabla(ABC):

    def __init__(self, archivoPrincipal = None): 
        
        self.archivoPrincipal = archivoPrincipal

    @abstractmethod
    def cargarDatos(self): pass

    @abstractmethod
    def definirFormato(self, contenedor1 = None, contenedor2 = None):  pass

    @abstractmethod
    def crearSentencia(self): pass