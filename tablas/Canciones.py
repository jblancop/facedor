'''
Clase que genera la secuencia INSERT correspondiente a la tabla "canciones" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Tabla

class Canciones(Tabla):

    def __init__(self, archivoPrincipal, archivoVotos, idLista):

        super().__init__(archivoPrincipal)
        self.archivoVotos = archivoVotos
        self.idLista = idLista

    def cargarDatos(self):

        campos = {} #Diccionario que almacena los cuatro campos de cada canción (el título, los votos recibidos y ambos enlaces de YouTube)
        datos = [] #Lista que almacena los 15 diccionarios correspondientes a cada una de las canciones
        
        arregloPrincipal = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción del título de la canción y de los enlaces de YouTube

        for linea in arregloPrincipal:

            if linea.find(').') != -1: campos['titulo_cancion'] = Extraer.cancion(linea) #Título
            if linea.find('tema:') != -1: campos['enlace_cancion_youtube'] = Extraer.enlace(linea) #Enlace principal           
            
            if linea.find('alternativo:') != -1: #En cada iteración, el vídeo alternativo va a ser lo último que encuentre

                campos['enlace_alternativo'] = Extraer.enlace(linea)

                datos.append(campos.copy()) #Se carga el diccionario (con tres pares clave/valor) al final de la lista

        arregloVotos = Utilidades.convertirArchivo(self.archivoVotos) #Extracción de los votos por canción

        votos = None #Es necesario iniciar la variable de algún modo aunque de primeras la función "votos()" sí va a encontrar un valor

        for linea in arregloVotos:

            cancion = Extraer.cancion(linea) #Se busca de nuevo el título de la canción para encontrar la equivalencia en "datos"
            votos = Extraer.votos(linea, votos)

            for campos in datos:

                if cancion.strip() == campos['titulo_cancion']: campos['votos_facebook'] = votos #Cuando encuentra la equivalencia, añade el cuarto par clave/valor al diccionario con el número de votos
    
        return datos
    
    def definirFormato(self, campos):

        c1 = campos['titulo_cancion']
        c2 = campos['votos_facebook']
        c3 = campos['enlace_cancion_youtube']
        c4 = campos['enlace_alternativo']

        formato = f'(NULL, "{c1}", {c2}, {0}, NULL, "{c3}", {0}, NULL, "{c4}", NULL, {self.idLista}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO canciones(id_cancion, titulo_cancion, votos_facebook, votos_web, nota_media, enlace_cancion_youtube, bloqueado, enlace_si_bloqueo, enlace_alternativo, enlace_alternativo_si_bloqueo, id_lista_spotify) VALUES' + '\n'
        cuerpo = ''
        datos = self.cargarDatos()
        contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

        for campos in datos:

            cuerpo += Utilidades.formateador(self.definirFormato(campos), contador)
            contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia