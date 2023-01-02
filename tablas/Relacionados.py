'''
Clase que genera la secuencia INSERT correspondiente a la tabla "relacionados" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Relacionados:

    def __init__(self, archivoEntrada): self.archivoEntrada = archivoEntrada

    def __str__(self):

        ENCABEZADO = 'INSERT INTO relacionados(id_disco, id_subestilo) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los subestilos presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            duo = {} #Diccionario que almacena el id del disco y los ids de los subestilos que le corresponden
            datos = [] #Lista que almacena los diccionarios
            contador = 0 #Contador de ids de subestilos

            for linea in arreglo:

                if linea.find(').') != -1: #Extracción del título del disco y búsqueda de su id en la BD

                    disco = Utilidades.disco(linea)

                    duo['id_disco'] = Modelo.listarId('id_disco', 'discos', 'titulo_disco', f'"{disco}"')

                if linea.find('Subestilos') != -1: #Extracción de los subestilos correspondientes y búsqueda de sus ids en la BD

                    conjunto = [] #Lista que almacena los ids de los subestilos y que luego se carga en duo como valor de la clave 'id_subestilos'

                    subestilos = Utilidades.subestilos(linea) #Lista con los subestilos de cada canción

                    for subestilo in subestilos:

                        idSubestilo = Modelo.listarId('id_subestilo', 'subestilos', 'nombre_subestilo', f'"{subestilo.strip()}"')

                        conjunto.append(idSubestilo)
                        contador += 1 #El número de sentencias a insertar depende del número total de subestilos

                    duo['id_subestilos'] = conjunto

                    datos.append(duo)

                    duo = {} #Es necesario borrar "duo" tras cada iteración porque "datos" no guarda sus valores sino una referencia al objeto

        for duo in datos:

            conjunto = duo['id_subestilos']

            for idSubestilo in conjunto:

                parametro1 = duo['id_disco']

                formato = f'({parametro1}, {idSubestilo}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia