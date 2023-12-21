'''
Clase que genera la secuencia INSERT correspondiente a la tabla "relacionados" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Modelo, Tabla

class Relacionados(Tabla):

    def __init__(self, archivoPrincipal): 
        
        super().__init__(archivoPrincipal)

    def cargarDatos(self):

        campos = {} #Diccionario que almacena el id del disco (clave) y los ids de los subestilos que le corresponden (valor; en realidad, una lista de valores)
        datos = [] #Lista que almacena los diccionarios
        
        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los subestilos presentes en el recopilatorio

        contador = 0 #Contador de ids de subestilos

        for linea in arreglo:

            if linea.find(').') != -1: #Extracción del título del disco y búsqueda de su id en la BD

                disco = Extraer.disco(linea)

                campos['id_disco'] = Modelo.listarId('id_disco', 'discos', 'titulo_disco', f'"{disco}"')

            if linea.find('Subestilos') != -1: #Extracción de los subestilos correspondientes y búsqueda de sus ids en la BD

                idsSubestilos = [] #Lista que almacena los ids de los subestilos y que luego se carga en campos como valor de la clave 'ids_subestilos'

                subestilos = Extraer.subestilos(linea) #Lista con los subestilos de cada canción

                for subestilo in subestilos:

                    idSubestilo = Modelo.listarId('id_subestilo', 'subestilos', 'nombre_subestilo', f'"{subestilo.strip()}"')

                    idsSubestilos.append(idSubestilo)
                    contador += 1 #El número de sentencias a insertar depende del número total de subestilos

                campos['ids_subestilos'] = idsSubestilos

                datos.append(campos.copy())

        return datos, contador
    
    def definirFormato(self, campos, idSubestilo):
        
        c1 = campos['id_disco']

        formato = f'({c1}, {idSubestilo}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO relacionados(id_disco, id_subestilo) VALUES' + '\n'
        cuerpo = ''
        datos, contador = self.cargarDatos()

        for campos in datos:

            idsSubestilos = campos['ids_subestilos']

            for idSubestilo in idsSubestilos:

                cuerpo += Utilidades.formateador(self.definirFormato(campos, idSubestilo), contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia