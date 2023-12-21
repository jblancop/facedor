'''
Clase que genera la secuencia INSERT correspondiente a la tabla "publican" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Modelo, Tabla

class Publican(Tabla):

    def __init__(self, archivoPrincipal): 
        
        super().__init__(archivoPrincipal)

    def cargarDatos(self):

        campos = {} #Diccionario que almacena los dos ids
        datos = [] #Lista que almacena los diccionarios
                
        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los artistas y discos presentes en el recopilatorio

        for linea in arreglo:

            if linea.find(').') != -1:

                artista = Extraer.artista(linea)
                disco = Extraer.disco(linea)

                campos['id_artista'] = Modelo.listarId('id_artista', 'artistas', 'nombre_artista', f'"{artista}"')
                campos['id_disco'] = Modelo.listarId('id_disco', 'discos', 'titulo_disco', f'"{disco}"')

                datos.append(campos.copy())

        return datos
    
    def definirFormato(self, campos):
        
        c1 = campos['id_artista']
        c2 = campos['id_disco']

        formato = f'({c1}, {c2}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO publican(id_artista, id_disco) VALUES' + '\n'
        cuerpo = ''
        datos = self.cargarDatos()
        contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

        for campos in datos:

            cuerpo += Utilidades.formateador(self.definirFormato(campos), contador)
            contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia