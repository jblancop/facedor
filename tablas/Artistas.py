'''
Clase que genera la secuencia INSERT correspondiente a la tabla "artistas" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Artistas:

    def __init__(self, archivoEntrada, artistasBD):

        self.archivoEntrada = archivoEntrada
        self.artistasBD = artistasBD

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO artistas(id_artista, nombre_artista, ano_debut, ano_retirada, enlace_rym, foto_artista, foto_alternativa, id_ciudad) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los artistas presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            sexteto = {} #Diccionario que almacena los seis campos correspondientes a cada artista
            datos = [] #Lista que almacena los diccionarios

            for linea in arreglo:

                if linea.find('(') != -1: sexteto['nombre_artista'] = Utilidades.artista(linea) #Los parámetros están listados según su orden dentro de la secuencia INSERT, aunque la iteración no ocurre en ese mismo orden
                if linea.find('Debut: ') != -1: sexteto['ano_debut'] = Utilidades.anos(linea)
                if linea.find('Retirada: ') != -1: sexteto['ano_retirada'] = Utilidades.anos(linea)
                if linea.find('rateyourmusic') != -1: sexteto['enlace_rym'] = Utilidades.enlace(linea)
                
                if linea.find('Fotografía: ') != -1: #En cada iteración, la fotografía va a ser lo último que localice

                    sexteto['foto_artista'] = Utilidades.enlace(linea)

                    if sexteto['nombre_artista'] not in self.artistasBD: datos.append(sexteto.copy()) #Por eso la carga del diccionario en la lista ocurre en este punto

                if linea.find(').') != -1:

                    localizacion = Utilidades.localizacion(linea)

                    ciudad = localizacion[0].strip()
                    pais = localizacion[1].strip()

                    sexteto['id_ciudad'] = Modelo.listarIdCiudad(ciudad, pais)

        contador = len(datos) #Número de elementos

        if contador == 0: cuerpo = 'No hay artistas nuevos que incorporar a la base de datos.'
        else:

            for sexteto in datos:

                parametro1 = sexteto['nombre_artista']
                parametro2 = sexteto['ano_debut']
                parametro3 = sexteto['ano_retirada']
                parametro4 = sexteto['enlace_rym']
                parametro5 = sexteto['foto_artista']
                parametro6 = sexteto['id_ciudad']

                formato = f'(NULL, "{parametro1}", {parametro2}, {parametro3}, "{parametro4}", "{parametro5}", NULL, {parametro6}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia