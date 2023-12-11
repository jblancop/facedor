'''
Clase que genera la secuencia INSERT correspondiente a la tabla "paises" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades

class Paises:

    def __init__(self, archivoEntrada, paisesBD, paisesBritanicos):

        self.archivoEntrada = archivoEntrada
        self.paisesBD = paisesBD
        self.paisesBritanicos = paisesBritanicos

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO paises(id_pais, nombre_pais, reino_unido) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los países presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            paises = set() #Conjunto (no permite valores repetidos) para almacenar los países

            for linea in arreglo:

                if linea.find(').') != -1: localizacion = Utilidades.localizacion(linea)

                pais = localizacion[1].strip()

                paises.add(pais)

        paisesNuevos = paises - self.paisesBD #Al ser conjuntos una simple resta permite saber qué países no están presentes en la BD

        contador = len(paisesNuevos) #Número de elementos

        if contador == 0: cuerpo = 'No hay países nuevos que incorporar a la base de datos.'
        else:

            for pais in paisesNuevos:

                if pais in self.paisesBritanicos: formato = f'(NULL, "{pais}", {1}),'
                else: formato = f'(NULL, "{pais}", {0}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia