'''
Clase que genera la secuencia INSERT correspondiente a la tabla "agrupados" de la BD
'''

from auxiliares import Utilidades
from infraestructura import Modelo, Tabla

class Agrupados(Tabla):

    def __init__(self, numeroSubestilos, estilos):

        super().__init__()
        self.numeroSubestilos = numeroSubestilos
        self.estilos = estilos

    def cargarDatos(self):
        
        datos = Modelo.listarUltimosSubestilos(self.numeroSubestilos) #Lista con tuplas (id_subestilo, nombre_subestilo)

        return datos

    def definirFormato(self, idSubestilo, estilo):

        if estilo == None: formato = f'(id_estilo, {idSubestilo}),'
        else:
        
            idEstilo = Modelo.listarIdEstilo(estilo)

            formato = f'({idEstilo}, {idSubestilo}),'

        return formato

    def crearSentencia(self):

        ENCABEZADO = 'INSERT INTO agrupados(id_estilo, id_subestilo) VALUES' + '\n'
        cuerpo = ''

        if self.numeroSubestilos == 0: cuerpo = 'No hay nuevos subestilos que agrupar.'
        else:

            datos = self.cargarDatos()
            
            contadorExterno = len(datos) * 2 #Se añaden dos líneas por subestilo en previsión de que un subestilo pueda estar relacionado con más de un estilo

            for tupla in datos: #Para cada nuevo subestilo

                idSubestilo = tupla[0]
                nombreSubestilo = tupla[1]

                contadorInterno = 0 #Se encarga de contar el número de equivalencias (subestilo/estilo) encontradas

                for estilo in self.estilos: #Para todos los estilos posibles

                    if nombreSubestilo.find(estilo) != -1: #Si el subestilo incorpora el estilo en su nombre, se da una equivalencia

                        cuerpo += Utilidades.formateador(self.definirFormato(idSubestilo, estilo), contadorExterno)
                        contadorExterno -= 1 #En cada iteración se reduce en uno el contador externo para cambiar "," por ";" cuando se llegue a la última línea
                        contadorInterno += 1 #Dado que se ha encontrado una equivalencia, el contador interno aumenta en 1

                if contadorInterno == 1: #Si sólo se ha encontrado una equivalencia, se añade otra línea por si es necesario relacionar el subestilo con otro estilo

                    cuerpo += Utilidades.formateador(self.definirFormato(idSubestilo, None), contadorExterno)
                    contadorExterno -= 1

                if contadorInterno == 0: #Si no se ha podido identificar ninguna equivalencia, añade dos líneas

                    cuerpo += Utilidades.formateador(self.definirFormato(idSubestilo, None), contadorExterno) * 2
                    contadorExterno -= 2 #Como se van a añadir dos líneas, se reduce en 2 el contador externo

        sentencia = ENCABEZADO + cuerpo

        return sentencia