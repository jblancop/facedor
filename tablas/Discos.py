'''
Clase que genera la secuencia INSERT correspondiente a la tabla "discos" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Discos:

    def __init__(self, archivoEntrada): 
        
        self.archivoEntrada = archivoEntrada

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO discos(id_disco, titulo_disco, tipo, id_cancion) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los discos presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            trio = {} #Diccionario que almacena los tres campos correspondientes a cada disco
            datos = [] #Lista que almacena los diccionarios (es decir, los discos)

            for linea in arreglo:

                if linea.find(').') != -1:

                    cancion = Utilidades.cancion(linea)

                    trio['titulo_disco'] = Utilidades.disco(linea)
                    trio['tipo'] = Utilidades.tipo(linea)
                    trio['id_cancion'] = Modelo.listarId('id_cancion', 'canciones', 'titulo_cancion', f'"{cancion}"')

                    datos.append(trio.copy())

            contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

            for trio in datos:

                parametro1 = trio['titulo_disco']
                parametro2 = trio['tipo']
                parametro3 = trio['id_cancion']

                formato = f'(NULL, "{parametro1}", "{parametro2}", {parametro3}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

            sentencia = ENCABEZADO + cuerpo

            return sentencia