'''
Clase con métodos estáticos de diversa índole
'''

from gestores import GestorInserciones as GI, GestorArchivos as GA

class Utilidades:

    @staticmethod #Parte final del proceso de principal.py
    def resolucionProceso(archivoSalida, sql, fase):

        print(GI.escribirSentencia(sql)) #Devuelve "Se ha escrito la sentencia INSERT..."

        input('Si todo está en orden, presiona "Intro" para insertar la sentencia consolidada en la base de datos.')

        inserciones = GI.insertarSentencia()

        if inserciones != None:

            print(f'Se ha(n) insertado {inserciones} registro(s).') #Indica cuántas filas -si alguna- se han insertado en la tabla

            GI.copiarArchivos(archivoSalida, fase)

            try: fase = GI.determinarFase() #Se comprueba cuál ha sido la última tabla poblada
            except: fase = None #Si el archivo temporal ni siquiera existe (es decir, se va a comenzar desde cero) se establece "fase" a None

            if fase == 'subestilos': GI.escribirSubestilos(inserciones)
            if fase == 'agrupados': GI.eliminarArchivos()

        else:

            print('Es necesario reiniciar esta fase.')

            try: fase = GI.determinarFase() #Se comprueba cuál ha sido la última tabla poblada
            except: fase = None #Si el archivo temporal ni siquiera existe (es decir, se va a comenzar desde cero) se establece "fase" a None

        return fase

    @staticmethod #Da el formato apropiado a la sentencia INSERT
    def formateador(formato, contador):

        if formato.find('"-1"') != -1: formato = formato.replace('"-1"', 'NULL') #Si encuentra un "-1" (cadena) lo sustituye por NULL
        if formato.find('-1') != -1: formato = formato.replace('-1', 'NULL') #Si encuentra un -1 (entero) lo sustituye por NULL

        if contador == 1: formato = formato.replace('),', ');') #Si el contador llega a 1 significa que es la última línea de la sentencia SQL
        else: formato = formato + '\n'

        return formato
    
    @staticmethod
    def convertirArchivo(archivoEntrada): #Convierte un archivo -del directorio "entradas"- en una matriz unidimensional de líneas

        with GA(archivoEntrada, 'r') as archivo:

            arreglo = archivo.read().splitlines() #Carga el archivo línea a línea

            return arreglo