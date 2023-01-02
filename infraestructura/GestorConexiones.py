'''
Clase (gestor de contexto con los métodos mágicos __enter__ y __exit__) para la conexión a MySQL
'''

import mysql.connector as mysql #Conector específico para MySQL

class GestorConexiones:

    INSTANCIA = {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'recopilatorios_pruebas'} #Parámetros de conexión

    @classmethod #Método que se invoca al comenzar la declaración "with"
    def __enter__(cls):

        cls.conexion = mysql.connect(**cls.INSTANCIA, buffered = True) #Se crea la conexión ("**" indica que se trata de un diccionario)
        cls.cursor = cls.conexion.cursor() #Y a partir de ella, el cursor, que es el que ejecuta las consultas sobre la BD

        return cls.cursor #La declaración "with" llama a esta clase, que devuelve el cursor

    @classmethod #Método que se invoca al finalizar la declaración "with"
    def __exit__(cls, tipoError, valorError, trazaError):

        if tipoError: #Si ocurre un error (valor distinto de "None") mientras se intenta realizar la operación sobre la BD

            cls.conexion.rollback() #Se deshace toda la operación y se notifica el tipo y el valor del error

            print(f'Ha ocurrido un error y se ha revertido la transacción en la base de datos: (1) {tipoError} (2) {valorError}')

            return True #Si no se devuelve "True" es necesario incluir el bloque "with" dentro de un "try/except"

        else: cls.conexion.commit() #De lo contrario, se acomete la operación

        cls.cursor.close() #Cierre del cursor
        cls.conexion.close() #Cierre de la conexión