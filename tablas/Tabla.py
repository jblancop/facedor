from abc import ABC, abstractmethod

def Tabla(ABC):

    @abstractmethod
    def cargarDatos(self):
        pass

    @abstractmethod
    def definirFormato(self):
        pass

    @abstractmethod
    def crearSentencia(self):
        pass