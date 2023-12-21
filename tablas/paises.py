'''
Clase que genera la secuencia INSERT correspondiente a la tabla "paises" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Tabla

class Paises(Tabla):

    def __init__(self, archivoPrincipal, paisesBD, paisesBritanicos):

        super().__init__(archivoPrincipal)
        self.paisesBD = paisesBD
        self.paisesBritanicos = paisesBritanicos

    def cargarDatos(self):

        paises = set() #Conjunto (no permite valores repetidos) para almacenar los países

        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los países presentes en el recopilatorio

        for linea in arreglo:

            if linea.find(').') != -1: localizacion = Extraer.localizacion(linea)

            pais = localizacion[1].strip()

            paises.add(pais)

        paisesNuevos = paises - self.paisesBD #Al ser conjuntos una simple resta permite saber qué países no están presentes en la BD

        return paisesNuevos

    def definirFormato(self, pais):

        if pais in self.paisesBritanicos: formato = f'(NULL, "{pais}", {1}),'
        else: formato = f'(NULL, "{pais}", {0}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO paises(id_pais, nombre_pais, reino_unido) VALUES' + '\n'
        cuerpo = ''
        paisesNuevos = self.cargarDatos()
        contador = len(paisesNuevos) #Número de elementos

        if contador == 0: cuerpo = 'No hay países nuevos que incorporar a la base de datos.'
        else:

            for pais in paisesNuevos:

                cuerpo += Utilidades.formateador(self.definirFormato(pais), contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia