'''
Clase que genera la secuencia INSERT correspondiente a la tabla "listas_spotify" de la BD
'''

class Listas:

    def __init__(self, ano, enlaceSpotify):

        self.ano = ano
        self.enlaceSpotify = enlaceSpotify

    def __str__(self):

        ENCABEZADO = 'INSERT INTO listas_spotify(id_lista_spotify, ano, enlace_spotify) VALUES' + '\n'
        cuerpo = f'(NULL, {self.ano}, "{self.enlaceSpotify}");'

        sentencia = ENCABEZADO + cuerpo

        return sentencia