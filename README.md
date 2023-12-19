# Facedor

Aplicación de consola interactiva para poblar la base de datos MySQL de **50 Años de Era Pop**.

## 1. Funcionamiento

Ejecutar en un terminal apropiado (el CMD de Windows, por ejemplo) y seguir las instrucciones que aparezcan en pantalla.

El directorio *entradas* (omitido gracias al archivo *.gitignore*) contiene dos tipos de archivos:

- año.txt
- votos_año.txt

*año.txt* (por ejemplo, *1963.txt*) contiene información sobre cada una de las 15 canciones del recopilatorio correspondiente al año en cuestión; cada bloque de información sigue la siguiente plantilla:

>"Lonely sea", de The Beach Boys (Hawthorne, EEUU). Extraído de su LP "Surfin' USA".
>
>El tema: https://www.youtube.com/watch?v=cQ9GiBxwCJI<br>
>Vídeo alternativo: https://www.youtube.com/watch?v=abQKew8eoRM
>
>El artista: https://rateyourmusic.com/artist/the-beach-boys
>
>Subestilos: Surf Rock, Vocal Surf, Rock & Roll, Doo-Wop
>
>Debut: 1961<br>
>Retirada: -1
>
>Fotografía: https://bit.ly/3PLjo4r

*votos_año.txt* (por ejemplo, *votos_1963.txt*) incluye los votos obtenidos por cada canción en diferentes redes sociales, con el siguiente formato:

>1\. The Beatles - "Please, please me" (8 votos)<br>
>2\. The Beach Boys - "Lonely sea" (5 votos)<br>
>=\. Bob Dylan - "Blowin' in the wind"<br>
>4\. Lonnie Mack - "Why" (3 votos)<br>
>=\. The Chiffons - "He's so fine"<br>
>6\. The Crystals - "Then he kissed me" (2 votos)<br>
>=\. Del Shannon - "Hats off to Larry"<br>
>=\. Elvis Presley - "(You're the) Devil in disguise"<br>
>9\. Roy Orbison - "In dreams" (1 voto)<br>
>=\. Randy & The Rainbows - "Denise"<br>
>=\. Martha & The Vandellas - "Heat wave"<br>
>=\. Dionne Warwick - "I smiled yesterday"<br>
>13\. The Surfaris - "Wipe out" (0 votos)<br>
>=\. Skeeter Davis - "The end of the world"<br>
>=\. The Chantays - "Pipeline"<br>

**Facedor** recorre ambos archivos y extrae la información pertinente para poblar cada una de las tablas de la BD mediante sentencias INSERT. El código SQL se imprime en dos archivos diferentes dentro del directorio *salidas* (omitido gracias al archivo *.gitignore*):

- sentencia.txt
- inserciones_año.txt

*sentencia.txt* es un archivo temporal que refleja la sentencia INSERT que acaba de ser condificada y que, una vez confirmada por el usuario, se ejecuta automáticamente sobre la BD. *inserciones_año.txt* (por ejemplo, *inserciones_1963.txt*) es un archivo persistente que sirve de registro de todas las sentencias introducidas en la BD para el recopilatorio en cuestión.

## 2. Estructura de directorios 

### 2.1. *infraestructura*

- **Modelo**: Clase con métodos estáticos que interaccionan con la BD.
- **Tabla**: Clase abstracta que sirve de plantilla para todas las clases que representan tablas de la BD.

### 2.2. *gestores*

- **GestorArchivos**: Clase gestor de contexto para el manejo de archivos .txt.
- **GestorConexiones**: Clase gestor de contexto para la conexión a la BD.
- **GestorInserciones**: Clase para la gestión de la escritura de las sentencias INSERT en los archivos .txt y en la BD.

### 2.3. *tablas*

Clases que representan las tablas a poblar de la BD y que generan, cada una de ellas, la secuencia INSERT correspondiente.

### 2.4. *auxiliares*

- **Extraer**: Clase con métodos estáticos para la extracción de información sobre las canciones.
- **Utilidades**: Clase con métodos estáticos de diversa índole.

## 3. Control de versiones:

- Insert Maker 1.0 (2018): Guion PHP funcional
- Facedor 2.0 (2022): Aplicación Python OO
- Facedor 2.1 (2023): Refactorización SOLID