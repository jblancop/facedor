'''
Clase con métodos estáticos de uso repetido
'''

from infraestructura.GestorInserciones import GestorInserciones as GI

class Utilidades:

    @staticmethod #Parte final, que siempre se repite, de cada etapa condicional de principal.py -equivalente a un require() en PHP-
    def repeticion(archivoSalida):

        input('Si todo está en orden, presiona "Intro" para insertar la sentencia consolidada en la base de datos.')

        inserciones = GI.insertarSentencia()

        if inserciones != None:

            print(f'Se ha(n) insertado {inserciones} registro(s).') #Indica cuántas filas -si alguna- se han insertado en la tabla

            GI.copiarArchivos(archivoSalida)

            fase = None

            try: fase = GI.determinarFase() #Se comprueba cuál ha sido la última tabla poblada
            except Exception as error: pass #Si el archivo temporal ni siquiera existe (es decir, se va a comenzar desde cero) se omite el paso

            if fase == 'subestilos': GI.escribirSubestilos(inserciones)
            if fase == 'agrupados': GI.eliminarArchivos()

            return fase

        else:

            print('Es necesario reiniciar esta fase.')

            fase = None

            try: fase = GI.determinarFase() #Se comprueba cuál ha sido la última tabla poblada
            except Exception as error: pass #Si el archivo temporal ni siquiera existe (es decir, se va a comenzar desde cero) se omite el paso

            return fase

    @staticmethod #Da el formato apropiado a la sentencia INSERT
    def formateador(formato, contador):

        if formato.find('"-1"') != -1: formato = formato.replace('"-1"', 'NULL') #Si encuentra un "-1" (cadena) lo sustituye por NULL
        if formato.find('-1') != -1: formato = formato.replace('-1', 'NULL') #Si encuentra un -1 (entero) lo sustituye por NULL

        if contador == 1: formato = formato.replace('),', ');') #Si el contador llega a 1 significa que es la última línea de la sentencia SQL
        else: formato = formato + '\n'

        return formato

    @staticmethod #Extrae el título de las canciones; pistas es un buleano con valor True si la extracción se hace a partir del archivo "pistas_xxxx"
    def cancion(pistas, linea):

        if pistas == True:

            inicio = linea.find(' - ') + 3 #El título siempre está 3 posiciones después del guión
            cancion = linea[inicio:].strip() #Se le aplica un limpiado de espacios en blanco

            return cancion

        else:

            trozos = linea.split('"') #Parte la cadena en función de las comillas dobles que encuentre

            cancion = trozos[1] #El título de la canción estará en la posición 1 de la lista resultante

            return cancion

    @staticmethod #Extrae enlaces https
    def enlace(linea):

        inicio = linea.find('https')

        if inicio != -1: #Si no hay enlace no va a localizar 'https' sino, generalmente, un '-1', por lo que find() devolverá un -1

            enlace = linea[inicio:].strip()

            return enlace

        else: return '-1' #Y a su vez se devolverá '-1', que la función formateador() transformará en NULL

    @staticmethod #Extrae los votos recibidos
    def votos(linea, votos):

        if linea.rfind(' voto') != -1: #Si localiza la expresión " voto" (empezando a buscar por la derecha), procede a extraer el número de votos

            inicio = linea.rfind(' (') + 2 #Delimitadores del voto
            fin = linea.rfind(' voto')

            votos = linea[inicio:fin]

            return votos

        else: return votos #Si no la localiza, utiliza el último valor encontrado; de ahí que necesite incorporarlo como parámetro del método

    @staticmethod #Extrae la pista que corresponde a cada canción en el recopilatorio
    def pista(linea):

        pista = linea[0:2]

        return pista

    @staticmethod #Extrae la localización del artista
    def localizacion(linea):

        particion = linea.split('", de ') #Parte la línea en dos para procesar sólo el segundo elemento y evitar confusiones con los paréntesis (en caso de que el título de la canción lleve alguno)

        inicio = particion[1].find(' (') + 2
        final = particion[1].find(').')

        localizacion = particion[1][inicio:final]

        localizacionTupla = tuple(localizacion.split(', ')) #Tupla con la ciudad como 1er elemento y el país como 2o

        return localizacionTupla

    @staticmethod #Extrae el nombre del autor
    def autor(linea):

        particion = linea.split('", de ') #Parte la línea en dos para procesar sólo el segundo elemento y evitar confusiones con los paréntesis

        inicio = 0
        final = particion[1].find(' (')

        autor = particion[1][inicio:final].strip()

        if autor != 'The The': #Si el autor no es 'The The'

            if autor.find('The') == 0: autor = autor[4:] + ', The' #Si el nombre empieza por 'The', recorta el artículo y le añade ', The' al final

        return autor

    @staticmethod #Extrae tanto el año de debut como el de retirada -si procede-
    def anos(linea):

        inicio = linea.find(': ') + 2

        ano = linea[inicio:].strip()

        return ano

    @staticmethod #Extrae el título del disco
    def disco(linea):

        trozos = linea.split('"')

        disco = trozos[3] #El índice cero está vacío, por lo que el título pasa a estar en cuarta y no en tercera posición

        return disco

    @staticmethod #Extrae el tipo de disco (LP, EP, sencillo o recopilatorio)
    def tipo(linea):

        trozos = linea.split('"')

        trozo = trozos[2].strip() #El índice cero está vacío, por lo que el tipo pasa a estar en tercera y no en segunda posición

        trocitos = trozo.split(' ')

        tipo = trocitos.pop() #El tipo de disco siempre es el último elemento de la lista

        if tipo not in ['LP', 'EP']: tipo = tipo.capitalize() #Convierte a máyusculas los tipos que no sean LP o EP

        return tipo

    @staticmethod #Extrae los subestilos (en forma de lista) asociados a cada canción
    def subestilos(linea):

        subestilosCadena = linea[12:]

        subestilosLista = subestilosCadena.split(', ')

        return subestilosLista