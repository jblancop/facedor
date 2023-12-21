'''
Clase que genera la secuencia INSERT correspondiente a la tabla "subestilos" de la BD
'''

from auxiliares import Extraer, Utilidades
from infraestructura import Tabla

class Subestilos(Tabla):

    def __init__(self, archivoPrincipal, subestilosBD):

        super().__init__(archivoPrincipal)
        self.subestilosBD = subestilosBD

    def cargarDatos(self):

        subestilosRecopilatorio = set() #Conjunto (no permite valores repetidos) para almacenar los subestilos del recopilatorio

        arreglo = Utilidades.convertirArchivo(self.archivoPrincipal) #Extracción de los subestilos presentes en el recopilatorio

        for linea in arreglo:

            if linea.find('Subestilos') != -1:

                subestilosCancion = Extraer.subestilos(linea) #Lista con los subestilos de cada canción

                for subestilo in subestilosCancion: subestilosRecopilatorio.add(subestilo.strip())

        subestilosNuevos = subestilosRecopilatorio - self.subestilosBD #Al ser conjuntos una simple resta permite saber qué subestilos no están presentes en la BD

        return subestilosNuevos
    
    def definirFormato(self, subestilo):
        
        formato = f'(NULL, "{subestilo}"),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO subestilos(id_subestilo, nombre_subestilo) VALUES' + '\n'
        cuerpo = ''
        subestilosNuevos = self.cargarDatos()
        contador = len(subestilosNuevos) #Número de elementos

        if contador == 0: cuerpo = 'No hay subestilos nuevos que incorporar a la base de datos.'
        else:

            for subestilo in subestilosNuevos:

                cuerpo += Utilidades.formateador(self.definirFormato(subestilo), contador)
                contador -= 1 #En cada iteración se reduce en uno el contador para cambiar "," por ";" cuando se llegue a la última sentencia

        sentencia = ENCABEZADO + cuerpo

        return sentencia