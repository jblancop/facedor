'''
Clase para la gestión de la escritura de las sentencias INSERT en los archivos .txt y en la BD
'''

import os #Librería para la eliminación de archivos

from gestores import GestorArchivos as GA, GestorConexiones as GC

class GestorInserciones:

    ARCHIVO_SENTENCIA = 'salidas/sentencia.txt'
    ARCHIVO_FASE = 'salidas/fase.txt'
    ARCHIVO_SUBESTILOS = 'salidas/subestilos.txt'

    @classmethod #Determina cuál es la última tabla (que equivale a la "fase" de la estructura condicional del archivo principal.py) de la BD que se ha poblado
    def determinarFase(cls): 

        with GA(cls.ARCHIVO_FASE, 'r') as archivo:

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            encabezado = arreglo[0] #El nombre de la tabla siempre está en el 1er elemento de la lista

            inicio = 12 #Límites del nombre de la tabla
            final = encabezado.find('(')

            fase = encabezado[inicio:final] #Cadena con el nombre de la tabla

            return fase

    @classmethod #Escritura de la sentencia INSERT en "ARCHIVO_SENTENCIA"
    def escribirSentencia(cls, sql):

        with GA(cls.ARCHIVO_SENTENCIA, 'w') as archivo: 
            
            archivo.write(sql)

            return f'Se ha escrito la sentencia INSERT en la ruta "{cls.ARCHIVO_SENTENCIA}". Comprueba que es correcta y, en caso de corregirla, no te olvides de guardar los cambios presionando Ctrl + S.'

    @classmethod #Escritura de la sentencia INSERT consolidada en la BD
    def insertarSentencia(cls):

        with GA(cls.ARCHIVO_SENTENCIA, 'r') as archivo:

            sql = archivo.read()

            if sql.find('No hay ') != -1: return 0 #Se evita el intento de inserción, que daría un error en el gestor de conexiones
            else:

                try:

                    with GC() as cursor:

                        cursor.execute(sql)

                        inserciones = cursor.rowcount

                        return inserciones

                except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @classmethod #Traslada la sentencia INSERT consolidada de "ARCHIVO_SENTENCIA" al archivo de salida y a "ARCHIVO_FASE"
    def copiarArchivos(cls, archivoSalida, fase):

        with GA(cls.ARCHIVO_SENTENCIA, 'r') as archivo: copia = archivo.read()
        with GA(cls.ARCHIVO_FASE, 'w') as archivo: archivo.write(copia)
        
        with GA(archivoSalida, 'a') as archivo: 
            
            if fase == 'relacionados': archivo.write(copia)
            else: archivo.write(copia + '\n\n')

    @classmethod #Escritura del número de subestilos nuevos que se han encontrado en el recopilatorio actual en "ARCHIVO_SUBESTILOS"
    def escribirSubestilos(cls, subestilos):

        with GA(cls.ARCHIVO_SUBESTILOS, 'w') as archivo: archivo.write(str(subestilos))

    @classmethod #Determina cuántos subestilos se insertaron en la fase correspondiente
    def determinarSubestilos(cls):

        with GA(cls.ARCHIVO_SUBESTILOS, 'r') as archivo:

            arreglo = archivo.readlines() #Carga el archivo en una lista

            numSubestilos = int(arreglo[0])

            return numSubestilos

    @classmethod #Eliminación de los archivos temporales una vez se ha completado la inserción del recopilatorio
    def eliminarArchivos(cls):

        os.remove(cls.ARCHIVO_SENTENCIA)
        os.remove(cls.ARCHIVO_FASE)
        os.remove(cls.ARCHIVO_SUBESTILOS)

        print(f'Se han eliminado todos los archivos temporales.')

