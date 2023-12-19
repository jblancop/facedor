'''
Clase que genera la secuencia INSERT correspondiente a la tabla "artistas" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Modelo, Tabla

class Artistas(Tabla):

    def __init__(self, archivoPrincipal, artistasBD):

        super().__init__(archivoPrincipal)
        self.artistasBD = artistasBD

    def cargarDatos(self):

        campos = {} #Diccionario que almacena los seis campos correspondientes a cada artista
        datos = [] #Lista que almacena los diccionarios

        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los artistas presentes en el recopilatorio

        for linea in arreglo:

            if linea.find('(') != -1: campos['nombre_artista'] = Extraer.artista(linea) #Nombre
            if linea.find('Debut: ') != -1: campos['ano_debut'] = Extraer.anos(linea) #Año de debut
            if linea.find('Retirada: ') != -1: campos['ano_retirada'] = Extraer.anos(linea) #Año de retirada
            if linea.find('rateyourmusic') != -1: campos['enlace_rym'] = Extraer.enlace(linea) #Enlace de RYM

            if linea.find(').') != -1:

                localizacion = Extraer.localizacion(linea) #Ciudad y país

                ciudad = localizacion[0].strip()
                pais = localizacion[1].strip()

                campos['id_ciudad'] = Modelo.listarIdCiudad(ciudad, pais)

            if linea.find('Fotografía: ') != -1:

                campos['foto_artista'] = Extraer.enlace(linea) #Enlace de Bitly

                if campos['nombre_artista'] not in self.artistasBD: datos.append(campos.copy())
        
        return datos

    def definirFormato(self, campos):
        
        c1 = campos['nombre_artista']
        c2 = campos['ano_debut']
        c3 = campos['ano_retirada']
        c4 = campos['enlace_rym']
        c5 = campos['foto_artista']
        c6 = campos['id_ciudad']

        formato = f'(NULL, "{c1}", {c2}, {c3}, "{c4}", "{c5}", NULL, {c6}),'

        return formato
    
    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO artistas(id_artista, nombre_artista, ano_debut, ano_retirada, enlace_rym, foto_artista, foto_alternativa, id_ciudad) VALUES' + '\n'
        cuerpo = ''
        datos = self.cargarDatos()
        contador = len(datos) #Número de elementos

        if contador == 0: cuerpo = 'No hay artistas nuevos que incorporar a la base de datos.'
        else:

            for campos in datos:

                cuerpo += Utilidades.formateador(self.definirFormato(campos), contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia