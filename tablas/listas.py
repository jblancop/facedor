'''
Clase que genera la secuencia INSERT correspondiente a la tabla "listas_spotify" de la BD
'''

from infraestructura import Tabla

class Listas(Tabla):

    def __init__(self, ano, enlaceSpotify):

        super().__init__()
        self.ano = ano
        self.enlaceSpotify = enlaceSpotify

    def cargarDatos(self): 
        
        pass

    def definirFormato(self):
        
        formato = f'(NULL, {self.ano}, "{self.enlaceSpotify}");'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO listas_spotify(id_lista_spotify, ano, enlace_spotify) VALUES' + '\n'
        cuerpo = self.definirFormato()
        
        sentencia = ENCABEZADO + cuerpo

        return sentencia