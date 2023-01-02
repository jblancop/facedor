'''
Clase que genera la secuencia INSERT correspondiente a la tabla "agrupados" de la BD
'''

from infraestructura.Utilidades import Utilidades
from infraestructura.Modelo import Modelo

class Agrupados:

    def __init__(self, numeroSubestilos, estilos):

        self.numeroSubestilos = numeroSubestilos
        self.estilos = estilos

    def __str__(self):

        ENCABEZADO = 'INSERT INTO agrupados(id_estilo, id_subestilo) VALUES' + '\n'
        cuerpo = ''''''

        if self.numeroSubestilos == 0: cuerpo = 'No hay nuevos subestilos que agrupar.'
        else:

            datos = Modelo.listarUltimosSubestilos(self.numeroSubestilos) #Lista con tuplas (id_subestilo, nombre_subestilo)

            contadorExterno = len(datos) * 2 #Se añaden dos líneas por subestilo en previsión de que un subestilo pueda estar relacionado con más de un estilo

            for tupla in datos: #Para cada nuevo subestilo

                idSubestilo = tupla[0]
                nombreSubestilo = tupla[1]

                contadorInterno = 0 #Se encarga de contar el número de equivalencias (subestilo/estilo) encontradas

                for estilo in self.estilos: #Para todos los estilos posibles

                    if nombreSubestilo.find(estilo) != -1: #Si el subestilo incorpora el estilo en su nombre, se da una equivalencia

                        idEstilo = Modelo.listarIdEstilo(estilo)

                        formato = f'({idEstilo}, {idSubestilo}),'

                        linea = Utilidades.formateador(formato, contadorExterno)

                        contadorExterno -= 1 #En cada iteración se reduce en uno el contador externo para cambiar "," por ";" cuando se llegue a la última línea
                        contadorInterno += 1 #Dado que se ha encontrado una equivalencia, el contador interno aumenta en 1

                        cuerpo += linea

                if contadorInterno == 1: #Si sólo se ha encontrado una equivalencia, se añade otra línea por si es necesario relacionar el subestilo con otro estilo

                    formato = f'(id_estilo, {idSubestilo}),'

                    linea = Utilidades.formateador(formato, contadorExterno)
                    contadorExterno -= 1

                    cuerpo += linea

                if contadorInterno == 0: #Si no se ha podido identificar ninguna equivalencia, añade dos líneas

                    formato = f'(id_estilo, {idSubestilo}),'

                    linea = Utilidades.formateador(formato, contadorExterno)
                    contadorExterno -= 2 #Como se van a añadir dos líneas, se reduce en 2 el contador externo

                    cuerpo += linea * 2

        sentencia = ENCABEZADO + cuerpo

        return sentencia