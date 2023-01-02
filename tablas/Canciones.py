'''
Clase que genera la secuencia INSERT correspondiente a la tabla "canciones" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades

class Canciones:

    def __init__(self, archivoEntrada, archivoVotos, archivoPistas, idLista):

        self.archivoEntrada = archivoEntrada
        self.archivoVotos = archivoVotos
        self.archivoPistas = archivoPistas
        self.idLista = idLista

    def __str__(self):

        ENCABEZADO = 'INSERT INTO canciones(id_cancion, titulo_cancion, pista, votos_facebook, votos_web, nota_media, enlace_cancion_youtube, enlace_alternativo, id_lista_spotify) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción del título de la canción y de los enlaces de YouTube

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            trio = {} #Diccionario que almacena cada terna de valores
            datos = [] #Lista que almacena los 15 diccionarios

            for linea in arreglo:

                if linea.find(').') != -1: trio['titulo_cancion'] = Utilidades.cancion(False, linea) #Título
                if linea.find('tema:') != -1: trio['enlace_cancion_youtube'] = Utilidades.enlace(linea) #Enlace principal
                if linea.find('alternativo:') != -1: #En cada iteración, el vídeo alternativo va a ser lo último que encuentre

                    trio['enlace_alternativo'] = Utilidades.enlace(linea)

                    datos.append(trio) #Se carga el diccionario (con tres pares clave/valor) al final de la lista

                    trio = {} #Es necesario reiniciar "trio" tras cada iteración porque "datos" no guarda sus valores sino una referencia al objeto, con lo cual al final del bucle "datos" tiene 15 referencias idénticas a "trio" (es decir, la última terna de valores repetida 15 veces)

        with GA(self.archivoVotos, 'r') as archivo: #Extracción de los votos por canción

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            votos = None #Es necesario iniciar la variable de algún modo aunque de primeras la función "votos" sí va a encontrar un valor

            for linea in arreglo:

                cancion = Utilidades.cancion(False, linea) #Se busca de nuevo el título de la canción para encontrar la equivalencia en "datos"
                votos = Utilidades.votos(linea, votos)

                for trio in datos:

                    if cancion in trio['titulo_cancion']: trio['votos_facebook'] = votos #Cuando encuentra la equivalencia, añade un nuevo par clave/valor al diccionario con el número de votos

        with GA(self.archivoPistas, 'r') as archivo: #Extracción de la posición de la canción en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            for linea in arreglo:

                cancion = Utilidades.cancion(True, linea) #Se busca de nuevo el título de la canción para encontrar la equivalencia en "datos"
                pista = Utilidades.pista(linea)

                for cuarteto in datos: #Ahora ya no hay tres pares clave/valor por diccionario sino cuatro

                    if cancion in cuarteto['titulo_cancion']: cuarteto['pista'] = pista #Cuando encuentra la equivalencia, añade un nuevo par clave/valor al diccionario con el número de votos

        contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

        for quinteto in datos: #Ahora hay cinco pares clave/valor por diccionario

            parametro1 = quinteto['titulo_cancion']
            parametro2 = quinteto['pista']
            parametro3 = quinteto['votos_facebook']
            parametro4 = quinteto['enlace_cancion_youtube']
            parametro5 = quinteto['enlace_alternativo']

            formato = f'(NULL, "{parametro1}", "{parametro2}", {parametro3}, {0}, NULL, "{parametro4}", "{parametro5}", {self.idLista}),'

            linea = Utilidades.formateador(formato, contador)
            contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

            cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia