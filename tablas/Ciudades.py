'''
Clase que genera la secuencia INSERT correspondiente a la tabla "ciudades" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Modelo, Tabla

class Ciudades(Tabla):

    def __init__(self, archivoPrincipal, localizacionesBD):

        super().__init__(archivoPrincipal)
        self.localizacionesBD = localizacionesBD

    def cargarDatos(self): 

        localizaciones = set() #Conjunto (no permite valores repetidos) para almacenar las tuplas de localizaciones

        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de las localizaciones ciudad/país presentes en el recopilatorio 

        for linea in arreglo:

            if linea.find(').') != -1: localizacion = Extraer.localizacion(linea)

            localizaciones.add(localizacion)

        localizacionesNuevas = localizaciones - self.localizacionesBD #Al ser conjuntos una simple resta permite saber qué localizaciones no están presentes en la BD

        return localizacionesNuevas
    
    def definirFormato(self, localizacion):  
        
        idPais = Modelo.listarId('id_pais', 'paises', 'nombre_pais', f'"{localizacion[1]}"') #localizacion[1] equivale al país

        formato = f'(NULL, "{localizacion[0]}", {1}, {0}, {idPais}),' #localizacion[0] equivale a la ciudad

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO ciudades(id_ciudad, nombre_ciudad, artista, usuario, id_pais) VALUES' + '\n'
        cuerpo = ''
        localizacionesNuevas = self.cargarDatos()
        contador = len(localizacionesNuevas) #Número de elementos

        if contador == 0: cuerpo = 'No hay ciudades nuevas que incorporar a la base de datos.'
        else:

            for localizacion in localizacionesNuevas:

                cuerpo += Utilidades.formateador(self.definirFormato(localizacion), contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia