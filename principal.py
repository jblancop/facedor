'''
Facedor 2.0 (versión 1.0 desarrollada en PHP), aplicación de consola interactiva para poblar la base de datos MySQL de 50 Años de Era Pop.
Ejecutar en Pycharm, VS Code o en el CMD de Windows y seguir las instrucciones que aparezcan en pantalla.
'''

from infraestructura.GestorInserciones import GestorInserciones as GI #Clases infraestructura
from infraestructura.Modelo import Modelo
from infraestructura.Utilidades import Utilidades

from tablas.Listas import Listas #Clases que representan cada una de las tablas de la BD
from tablas.Canciones import Canciones
from tablas.Paises import Paises
from tablas.Ciudades import Ciudades
from tablas.Artistas import Artistas
from tablas.Discos import Discos
from tablas.Publican import Publican
from tablas.Subestilos import Subestilos
from tablas.Relacionados import Relacionados
from tablas.Agrupados import Agrupados

nombreAplicacion = 'Facedor'
bienvenida = f' Bienvenido a {nombreAplicacion}, la aplicación para poblar la base de datos MySQL de 50 Años de Era Pop '
advertencia = f'\nPulsa 0 si quieres salir de {nombreAplicacion} o cualquier otra tecla para continuar, y presiona "Intro": '

print('\n' + bienvenida.center(len(bienvenida) + 10, '#') + '\n')

escape = None #Variable que controla el bucle "while"
fase = None #Variable que controla la estructura condicional "if/elif"

try: fase = GI.determinarFase() #Se comprueba cuál ha sido la última tabla poblada
except Exception as error: pass #Si el archivo temporal ni siquiera existe (es decir, se va a comenzar desde cero) se omite el paso

if fase == None: #Si se comienza el proceso desde cero

    anoAnterior = Modelo.listarUltimoAno()
    ano = anoAnterior - 1

else: #Si se retoma desde la última tabla poblada

    ano = Modelo.listarUltimoAno()
    anoAnterior = ano + 1

    print(f'Estamos procesando el recopilatorio correspondiente a {ano}.')

archivoEntrada = f'entradas/{ano}.txt' #Archivos no temporales de entrada y salida
archivoVotos = f'entradas/votos_{ano}.txt'
archivoSalida = f'salidas/inserciones_{ano}.txt'

try:

    while escape != '0': #Mientras no se pulse 0, el bucle va haciendo avanzar el proceso de fase en fase gracias a la estructura condicional

        if fase == None: #Poblado de la tabla "listas_spotify"

            print(f'El último año registrado en la base de datos es {anoAnterior}, así que se va a procesar el recopilatorio correspondiente a {ano}.\n')
            print('1) Se va a generar la sentencia INSERT para la tabla "listas_spotify".')

            enlaceSpotify = input(f'Introduce el enlace de Spotify correspondiente a {ano}: ')

            lista = Listas(ano, enlaceSpotify) #Se crea el objeto lista
            
            sql = lista.crearSentencia()

        elif fase == 'listas_spotify': #Poblado de la tabla "canciones"

            print('\n2) Se va a generar la sentencia INSERT para la tabla "canciones".')

            idLista = Modelo.listarId('id_lista_spotify', 'listas_spotify', 'ano', ano)

            canciones = Canciones(archivoEntrada, archivoVotos, idLista) #Se crea el objeto canciones

            sql = canciones.crearSentencia()

        elif fase == 'canciones': #Poblado de la tabla "paises"

            print('\n3) Se va a generar la sentencia INSERT para la tabla "paises".')

            paisesBD = Modelo.listarElementos('nombre_pais', 'paises') #Todos los países presentes en la BD
            paisesBritanicos = {'Inglaterra', 'Escocia', 'Gales', 'Irlanda del Norte'}

            paises = Paises(archivoEntrada, paisesBD, paisesBritanicos) #Se crea el objeto paises

            sql = paises.crearSentencia()

        elif fase == 'paises': #Poblado de la tabla "ciudades"

            print('\n4) Se va a generar la sentencia INSERT para la tabla "ciudades".')

            localizacionesBD = Modelo.listarLocalizaciones() #Todas las localizaciones (ciudad, país) presentes en la BD

            ciudades = Ciudades(archivoEntrada, localizacionesBD) #Se crea el objeto ciudades

            sql = ciudades.crearSentencia()

        elif fase == 'ciudades': #Poblado de la tabla "artistas"

            print('\n5) Se va a generar la sentencia INSERT para la tabla "artistas".')

            artistasBD = Modelo.listarElementos('nombre_artista', 'artistas') #Todos los artistas presentes en la BD

            artistas = Artistas(archivoEntrada, artistasBD) #Se crea el objeto artistas

            sql = artistas.crearSentencia()

        elif fase == 'artistas': #Poblado de la tabla "discos"

            print('\n6) Se va a generar la sentencia INSERT para la tabla "discos".')

            discos = Discos(archivoEntrada) #Se crea el objeto discos

            sql = discos.crearSentencia()

        elif fase == 'discos': #Poblado de la tabla "publican"

            print('\n7) Se va a generar la sentencia INSERT para la tabla "publican".')

            publican = Publican(archivoEntrada) #Se crea el objeto publican

            sql = publican.crearSentencia()

        elif fase == 'publican': #Poblado de la tabla "subestilos"

            print('\n8) Se va a generar la sentencia INSERT para la tabla "subestilos".')

            subestilosBD = Modelo.listarElementos('nombre_subestilo', 'subestilos') #Todos los subestilos presentes en la BD

            subestilos = Subestilos(archivoEntrada, subestilosBD) #Se crea el objeto subestilos

            sql = subestilos.crearSentencia()

        elif fase == 'subestilos': #Poblado de la tabla "relacionados"

            print('\n9) Se va a generar la sentencia INSERT para la tabla "relacionados".')

            relacionados = Relacionados(archivoEntrada) #Se crea el objeto relacionados

            sql = relacionados.crearSentencia()

        elif fase == 'relacionados': #Poblado de la tabla "agrupados"

            print('\n10) Se va a generar la sentencia INSERT para la tabla "agrupados".')

            numeroSubestilos = GI.determinarSubestilos()
            estilos = ('Country', 'Electro', 'tronic', 'Folk', 'Metal', 'Pop', 'Punk', 'Rock', 'Blues', 'Jazz', 'Hip Hop')

            agrupados = Agrupados(numeroSubestilos, estilos) #Se crea el objeto agrupados

            sql = agrupados.crearSentencia()

        fase = Utilidades.resolucionProceso(archivoSalida, sql)
        
        if fase == 'agrupados': escape = '0'
        else: escape = input(advertencia)

    if fase == 'agrupados': print(f'\nHemos terminado con {ano}, así que... ¡Hasta el próximo recopilatorio!')
    else: print(f'\nLa última tabla poblada ha sido "{fase}".')

except Exception as error: print(f'Ha ocurrido un error: (1) {type(error)} (2) {error}')