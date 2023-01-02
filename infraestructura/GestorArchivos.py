'''
Clase (gestor de contexto) para el manejo de archivos .txt
'''

class GestorArchivos:

    def __init__(self, nombre, modo):

        self.nombre = nombre #En el método iniciador se pasa el nombre (y la ruta) del archivo a crear
        self.modo = modo #Y el modo en el que se abrirá el archivo (lectura: r, escritura: w, agregación: a)

    def __enter__(self): #Método que se invoca al comenzar la declaración "with"

        self.archivo = open(self.nombre, self.modo, encoding = 'utf8')

        return self.archivo

    def __exit__(self, tipoError, valorError, trazaError): #Método que se invoca al finalizar la declaración "with"

        self.archivo.close()

        if tipoError:

            print(f'Ha ocurrido un error al procesar el archivo: (1) {tipoError} (2) {valorError}')
            
            return True #Si no se devuelve "True" es necesario incluir el bloque "with" dentro de un "try/except"'''