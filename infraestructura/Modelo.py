'''
Clase con métodos estáticos que interaccionan con la base de datos
'''

from infraestructura.GestorConexiones import GestorConexiones as GC

class Modelo:

    @staticmethod #Determina cuál es el último año que aparece registrado en la tabla "listas_spotify"
    def listarUltimoAno():

        try:

            with GC() as cursor:

                sql = '''
                        SELECT 
                            min(ano) 
                        FROM 
                            listas_spotify
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchone() #Devuelve una tupla de un solo elemento

                return resultado[0]

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Devuelve un id concreto dada una condición
    def listarId(id, tabla, parametro, valor):

        try:

            with GC() as cursor:

                sql = f'''
                        SELECT 
                            {id} 
                        FROM 
                            {tabla}
                        WHERE
                            {parametro} = {valor}
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchone() #Devuelve una tupla de un solo elemento

                return resultado[0]

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Devuelve un conjunto de elementos del mismo tipo
    def listarElementos(parametro, tabla):

        try:

            with GC() as cursor:

                sql = f'''
                        SELECT 
                            {parametro} 
                        FROM 
                            {tabla}
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchall() #Devuelve una lista de tuplas de un solo elemento

                conjunto = set() #Se crea un conjunto (en algunos casos es necesario hacer una resta de conjuntos)

                for parametro in resultado: conjunto.add(parametro[0]) #Se rellena con los elementos individuales contenidos en la lista de tuplas

                return conjunto

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Determina qué localizaciones (ciudad/país) hay en la BD
    def listarLocalizaciones():

        try:

            with GC() as cursor:

                sql = '''
                        SELECT 
                            nombre_ciudad,
                            nombre_pais 
                        FROM 
                            ciudades 
                                NATURAL JOIN paises
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchall() #Devuelve una lista de tuplas de dos elementos

                return set(resultado) #Se convierte la lista en un conjunto

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Determina el id de la ciudad de la que es originario cada autor
    def listarIdCiudad(ciudad, pais):

        try:

            with GC() as cursor:

                sql = f'''
                        SELECT 
                            id_ciudad 
                        FROM 
                            ciudades
                                NATURAL JOIN paises  
                        WHERE
                            nombre_ciudad = "{ciudad}"
                            AND nombre_pais = "{pais}"
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchone() #Este método devuelve una tupla de un solo elemento

                return resultado[0]

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Determina qué subestilos se añadieron por última vez a la BD
    def listarUltimosSubestilos(numSubestilos):

        try:

            with GC() as cursor:

                sql = f'''
                        SELECT 
                            id_subestilo,
                            nombre_subestilo 
                        FROM 
                            subestilos 
                        ORDER BY
                            id_subestilo DESC
                        LIMIT {numSubestilos}
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchall() #Este método devuelve una lista de tuplas de dos elementos

                return resultado

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')

    @staticmethod #Determina el id del estilo en función de su nombre (o parte del nombre, de ahí el LIKE)
    def listarIdEstilo(estilo):

        try:

            with GC() as cursor:

                sql = f'''
                        SELECT 
                            id_estilo 
                        FROM 
                            estilos
                        WHERE
                            nombre_estilo LIKE "%{estilo}%"
                        '''

                cursor.execute(sql)

                resultado = cursor.fetchone() #Este método devuelve una tupla de un solo elemento

                return resultado[0]

        except Exception as error: print(f'Ha ocurrido un error relacionado con la base de datos: (1) {type(error)} (2) {error}')