'''
Clase que genera la secuencia INSERT correspondiente a la tabla "ciudades" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Ciudades:

    def __init__(self, archivoEntrada, localizacionesBD):

        self.archivoEntrada = archivoEntrada
        self.localizacionesBD = localizacionesBD

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO ciudades(id_ciudad, nombre_ciudad, artista, usuario, id_pais) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de las localizaciones ciudad/país presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            localizaciones = set() #Conjunto (no permite valores repetidos) para almacenar las tuplas de localizaciones

            for linea in arreglo:

                if linea.find(').') != -1: localizacion = Utilidades.localizacion(linea)

                localizaciones.add(localizacion)

        localizacionesNuevas = localizaciones - self.localizacionesBD #Al ser conjuntos una simple resta permite saber qué localizaciones no están presentes en la BD

        contador = len(localizacionesNuevas) #Número de elementos

        if contador == 0: cuerpo = 'No hay ciudades nuevas que incorporar a la base de datos.'
        else:

            for localizacion in localizacionesNuevas:

                idPais = Modelo.listarId('id_pais', 'paises', 'nombre_pais', f'"{localizacion[1]}"') #localizacion[1] equivale al país

                formato = f'(NULL, "{localizacion[0]}", {1}, {0}, {idPais}),' #localizacion[0] equivale a la ciudad

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia