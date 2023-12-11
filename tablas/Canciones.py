'''
Clase que genera la secuencia INSERT correspondiente a la tabla "canciones" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades

class Canciones:

    def __init__(self, archivoEntrada, archivoVotos, idLista):

        self.archivoEntrada = archivoEntrada
        self.archivoVotos = archivoVotos
        self.idLista = idLista

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO canciones(id_cancion, titulo_cancion, votos_facebook, votos_web, nota_media, enlace_cancion_youtube, bloqueado, enlace_si_bloqueo, enlace_alternativo, enlace_alternativo_si_bloqueo, id_lista_spotify) VALUES' + '\n'
        cuerpo = ''''''
        
        cuarteto = {} #Diccionario que almacena los cuatro campos de cada canción (el título, los votos recibidos y ambos enlaces de YouTube)
        datos = [] #Lista que almacena los 15 diccionarios (correspondientes a cada una de las canciones)

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción del título de la canción y de los enlaces de YouTube

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            for linea in arreglo:

                if linea.find(').') != -1: cuarteto['titulo_cancion'] = Utilidades.cancion(linea) #Título
                if linea.find('tema:') != -1: cuarteto['enlace_cancion_youtube'] = Utilidades.enlace(linea) #Enlace principal           
                if linea.find('alternativo:') != -1: #En cada iteración, el vídeo alternativo va a ser lo último que encuentre

                    cuarteto['enlace_alternativo'] = Utilidades.enlace(linea)

                    datos.append(cuarteto.copy()) #Se carga el diccionario (con tres pares clave/valor) al final de la lista

        with GA(self.archivoVotos, 'r') as archivo: #Extracción de los votos por canción

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            votos = None #Es necesario iniciar la variable de algún modo aunque de primeras la función "votos" sí va a encontrar un valor

            for linea in arreglo:

                cancion = Utilidades.cancion(linea) #Se busca de nuevo el título de la canción para encontrar la equivalencia en "datos"
                votos = Utilidades.votos(linea, votos)

                for cuarteto in datos:

                    if cancion in cuarteto['titulo_cancion']: cuarteto['votos_facebook'] = votos #Cuando encuentra la equivalencia, añade un nuevo par clave/valor al diccionario con el número de votos (ahora por fin ya es un cuarteto de valores)

        contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

        for cuarteto in datos:

            parametro1 = cuarteto['titulo_cancion']
            parametro2 = cuarteto['votos_facebook']
            parametro3 = cuarteto['enlace_cancion_youtube']
            parametro4 = cuarteto['enlace_alternativo']

            formato = f'(NULL, "{parametro1}", "{parametro2}", {0}, NULL, "{parametro3}", {0}, NULL, "{parametro4}", NULL, {self.idLista}),'

            linea = Utilidades.formateador(formato, contador)
            contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

            cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia