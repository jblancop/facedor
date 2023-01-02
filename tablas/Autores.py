'''
Clase que genera la secuencia INSERT correspondiente a la tabla "autores" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Autores:

    def __init__(self, archivoEntrada, autoresBD):

        self.archivoEntrada = archivoEntrada
        self.autoresBD = autoresBD

    def __str__(self):

        ENCABEZADO = 'INSERT INTO autores(id_autor, nombre_autor, ano_debut, ano_retirada, enlace_rym, foto_autor, foto_alternativa, id_ciudad) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los países presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            sexteto = {'foto_autor': -1} #Diccionario que almacena los seis campos correspondientes a cada autor (por defecto se incluye "foto_autor" con un -1 porque algunos archivos de entrada no incluyen este tipo de información)
            datos = [] #Lista que almacena los diccionarios

            for linea in arreglo:

                if linea.find('(') != -1: sexteto['nombre_autor'] = Utilidades.autor(linea) #Los parámetros están listados según su orden dentro de la secuencia INSERT, aunque la iteración no ocurre en ese mismo orden
                if linea.find('Debut: ') != -1: sexteto['ano_debut'] = Utilidades.anos(linea)
                if linea.find('Retirada: ') != -1: sexteto['ano_retirada'] = Utilidades.anos(linea)
                if linea.find('rateyourmusic') != -1: sexteto['enlace_rym'] = Utilidades.enlace(linea)
                if linea.find('Fotografía: ') != -1: #En cada iteración, la fotografía va a ser lo último que localice

                    sexteto['foto_autor'] = Utilidades.enlace(linea)

                    if sexteto['nombre_autor'] not in self.autoresBD: #Por eso la carga del diccionario en la lista ocurre en este punto

                        datos.append(sexteto)

                        sexteto = {'foto_autor': -1} #Es necesario reiniciar "sexteto" tras cada iteración porque "datos" no guarda sus valores sino una referencia al objeto

                if linea.find(').') != -1:

                    localizacion = Utilidades.localizacion(linea)

                    ciudad = localizacion[0].strip()
                    pais = localizacion[1].strip()

                    sexteto['id_ciudad'] = Modelo.listarIdCiudad(ciudad, pais)

        contador = len(datos) #Número de elementos

        if contador == 0: cuerpo = 'No hay autores nuevos que incorporar a la base de datos.'
        else:

            for sexteto in datos:

                parametro1 = sexteto['nombre_autor']
                parametro2 = sexteto['ano_debut']
                parametro3 = sexteto['ano_retirada']
                parametro4 = sexteto['enlace_rym']
                parametro5 = sexteto['foto_autor']
                parametro6 = sexteto['id_ciudad']

                formato = f'(NULL, "{parametro1}", {parametro2}, {parametro3}, "{parametro4}", "{parametro5}", NULL, {parametro6}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia