'''
Clase que genera la secuencia INSERT correspondiente a la tabla "publican" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Publican:

    def __init__(self, archivoEntrada): self.archivoEntrada = archivoEntrada

    def __str__(self):

        ENCABEZADO = 'INSERT INTO publican(id_autor, id_disco) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los autores y discos presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            duo = {} #Diccionario que almacena los dos ids
            datos = [] #Lista que almacena los diccionarios

            for linea in arreglo:

                if linea.find(').') != -1:

                    autor = Utilidades.autor(linea)
                    disco = Utilidades.disco(linea)

                    duo['id_autor'] = Modelo.listarId('id_autor', 'autores', 'nombre_autor', f'"{autor}"')
                    duo['id_disco'] = Modelo.listarId('id_disco', 'discos', 'titulo_disco', f'"{disco}"')

                    datos.append(duo)

                    duo = {} #Es necesario borrar "duo" tras cada iteración porque "datos" no guarda sus valores sino una referencia al objeto

            contador = len(datos) #Número de elementos; en este caso, siempre van a ser 15

            for duo in datos:

                parametro1 = duo['id_autor']
                parametro2 = duo['id_disco']

                formato = f'({parametro1}, {parametro2}),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

            sentencia = ENCABEZADO + cuerpo

            return sentencia