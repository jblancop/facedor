'''
Clase que genera la secuencia INSERT correspondiente a la tabla "subestilos" de la BD
'''

from infraestructura.GestorArchivos import GestorArchivos as GA
from infraestructura.Utilidades import Utilidades

class Subestilos:

    def __init__(self, archivoEntrada, subestilosBD):

        self.archivoEntrada = archivoEntrada
        self.subestilosBD = subestilosBD

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO subestilos(id_subestilo, nombre_subestilo) VALUES' + '\n'
        cuerpo = ''''''

        with GA(self.archivoEntrada, 'r') as archivo: #Extracción de los subestilos presentes en el recopilatorio

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            subestilosRecopilatorio = set() #Conjunto (no permite valores repetidos) para almacenar los subestilos del recopilatorio

            for linea in arreglo:

                if linea.find('Subestilos') != -1:

                    subestilosCancion = Utilidades.subestilos(linea) #Lista con los subestilos de cada canción

                    for subestilo in subestilosCancion: subestilosRecopilatorio.add(subestilo.strip())

        subestilosNuevos = subestilosRecopilatorio - self.subestilosBD #Al ser conjuntos una simple resta permite saber qué subestilos no están presentes en la BD

        contador = len(subestilosNuevos) #Número de elementos

        if contador == 0: cuerpo = 'No hay subestilos nuevos que incorporar a la base de datos.'
        else:

            for subestilo in subestilosNuevos:

                formato = f'(NULL, "{subestilo}"),'

                linea = Utilidades.formateador(formato, contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

                cuerpo += linea

        sentencia = ENCABEZADO + cuerpo

        return sentencia