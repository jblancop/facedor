'''
Clase que genera la secuencia INSERT correspondiente a la tabla "discos" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Modelo, Tabla

class Discos(Tabla):

    def __init__(self, archivoPrincipal): 
        
        super().__init__(archivoPrincipal)

    def cargarDatos(self):

        campos = {} #Diccionario que almacena los tres campos correspondientes a cada disco
        datos = [] #Lista que almacena los diccionarios
                
        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los discos presentes en el recopilatorio

        for linea in arreglo:

            if linea.find(').') != -1:

                cancion = Extraer.cancion(linea)

                campos['titulo_disco'] = Extraer.disco(linea)
                campos['tipo'] = Extraer.tipo(linea)
                campos['id_cancion'] = Modelo.listarId('id_cancion', 'canciones', 'titulo_cancion', f'"{cancion}"')

                datos.append(campos.copy())

        return datos
    
    def definirFormato(self, campos):
        
        c1 = campos['titulo_disco']
        c2 = campos['tipo']
        c3 = campos['id_cancion']

        formato = f'(NULL, "{c1}", "{c2}", {c3}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO discos(id_disco, titulo_disco, tipo, id_cancion) VALUES' + '\n'
        cuerpo = ''
        datos = self.cargarDatos()
        contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

        for campos in datos:

            cuerpo += Utilidades.formateador(self.definirFormato(campos), contador)
            contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia