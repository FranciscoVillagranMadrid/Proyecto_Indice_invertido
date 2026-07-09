# Sistema de Red Social con Índice Invertido, Grafo y Tabla Hash

Proyecto semestral para **ICI313 - Estructuras de Datos**.

El proyecto trabaja con datos de Reddit/Pushshift y modela una red social simple. La primera parte permite buscar posts por términos y contactos por usuario usando índices invertidos. La segunda parte agrega un grafo no dirigido de contactos y búsqueda por grados usando BFS. La tercera parte agrega una tabla hash propia para contar frecuencia de términos.

## Archivos principales

```text
listas.py              Nodos y listas enlazadas propias.
indices.py             Stopwords e índices invertidos de posts y usuarios.
grafo_contactos.py     Grafo no dirigido y BFS por grados.
tabla_hash.py          Tabla hash propia con djb2 y encadenamiento separado.
red_social.py          Programa principal y menú de prueba.
preprocesar_reddit.py  Archivo auxiliar para preparar el dataset original.
usuarios.csv           Usuarios ya preparados.
posts.csv              Posts ya preparados.
relaciones.csv         Relaciones/contactos ya preparados.
stopwords.txt          Palabras comunes que se filtran.
```

## Cómo ejecutar

```bash
python red_social.py
```

El programa carga los archivos CSV, construye los índices invertidos, construye el grafo, construye la tabla hash y muestra el menú principal.

## Entrega I: Índices invertidos

Se implementan dos índices principales:

```text
termino -> ListaPosts enlazada
usuario -> ListaUsuarios enlazada
```

Los diccionarios se usan como mapa para llegar rápido a la clave, pero los valores son listas enlazadas propias implementadas en `listas.py`.

También se usa un filtro de stopwords para eliminar palabras comunes antes de construir el índice y antes de procesar consultas.

## Entrega II: Grafo de contactos y BFS

El grafo se construye desde el índice de usuarios/contactos. Es un grafo no dirigido, por lo que si un usuario A está conectado con B, también se guarda la conexión de B hacia A.

La estructura usada es:

```text
usuario -> ListaUsuarios enlazada de vecinos
```

Además, al construir el grafo desde el sistema principal, cada vértice queda asociado a la referencia del objeto `Usuario` correspondiente. Esto mantiene la relación con los datos cargados desde la Entrega I y evita que el grafo sea una estructura separada sin contexto.

La búsqueda BFS permite mostrar contactos de:

```text
1° grado
2° grado
3° grado
```

El recorrido evita duplicados y evita que el usuario raíz aparezca como contacto de sí mismo. Cada nivel se ordena alfabéticamente solo al momento de mostrarlo, para que la demo sea más clara.

## Entrega III: Tabla hash de términos

Se implementa una tabla hash propia para contar frecuencia de términos. No se usa `dict` de Python como tabla hash.

Características:

```text
Función hash: djb2
Truncado a 32 bits: hash_val &= 0xFFFFFFFF
Colisiones: encadenamiento separado
Cada casilla: ListaTerminosHash enlazada
M: primer primo que cumple M >= 1.5 * N
```

La frecuencia se cuenta recorriendo el texto de los posts y agregando cada aparición válida del término. Se filtran stopwords, números solos y palabras muy cortas.

## Métricas que muestra el programa

```text
N: términos únicos
M: tamaño de la tabla hash
Factor de carga: N / M
Total de colisiones
Largo máximo de cadena
Promedio de cadenas no vacías
```

También permite consultar Top-N términos frecuentes para:

```text
Top 5
Top 10
Top 20
```

Cuando dos términos tienen la misma frecuencia, se ordenan alfabéticamente. Esto no cambia el conteo.

## Menú principal

```text
1. Buscar posts por termino / palabra clave
2. Buscar usuario y mostrar contactos directos
3. Mostrar algunos posts cargados
4. Mostrar resumen de carga
5. Buscar contactos por grado (BFS)
6. Mostrar Top-N terminos frecuentes
7. Mostrar metricas de tabla hash
8. Salir
```

## Adaptación del dataset Reddit

Reddit no entrega amigos directos como Facebook, por eso los contactos se modelan desde interacciones o co-participación. Además, Reddit entrega `score`, pero no entrega la identidad real de cada usuario que votó, por eso los likes se representan como likes simbólicos desde el score.

## Nota sobre memoria dinámica

Los límites de carga del dataset no vuelven estáticas las estructuras. Solo controlan cuántos datos se leen para la demostración. Los nodos de listas enlazadas, listas de adyacencia y cadenas de la tabla hash se crean durante la ejecución.

## Datos de defensa para Entrega II y III

### Parametros reales de esta ejecucion

Con los archivos incluidos en este proyecto, el programa reporta:

```text
Usuarios cargados          : 30
Posts cargados             : 50
Relaciones cargadas        : 64
Terminos indexados / N     : 304
Usuarios en el grafo       : 30
Aristas del grafo          : 32
M tabla hash               : 457
Factor de carga N/M        : 0.6652
Total de colisiones        : 91
Largo maximo de cadena     : 4
Promedio cadenas no vacias : 1.43
```

La relacion entre `Relaciones cargadas` y `Aristas del grafo` puede verse asi: en el archivo y en el indice se guarda cada contacto en ambos sentidos para asegurar la simetria, pero en el grafo cada amistad real se cuenta una sola vez como arista no dirigida. Por eso 64 relaciones dirigidas equivalen a 32 aristas no dirigidas.

### Complejidad del BFS

El BFS por grados usa una cola por niveles y marca los usuarios visitados para no repetirlos. En el peor caso, si alcanza muchos usuarios, su complejidad es:

```text
Tiempo: O(V + E)
Memoria: O(V)
```

Donde `V` es la cantidad de usuarios del grafo y `E` la cantidad de relaciones/aristas. En este proyecto se corta en grado 3 porque la pauta solo pide contactos de 1°, 2° y 3° grado.

### Funciones principales para defender

```text
GrafoContactos.agregar_contacto()          agrega aristas en ambos sentidos
GrafoContactos.construir_desde_indice()    arma el grafo desde el indice de usuarios
GrafoContactos.obtener_contactos_grado()   aplica BFS por niveles hasta grado 3
GrafoContactos.validar_simetria()          comprueba que A-B tambien exista como B-A
TablaHashTerminos.calcular_hash()          implementa djb2 con truncado a 32 bits
TablaHashTerminos.construir()              cuenta apariciones reales de terminos
TablaHashTerminos.obtener_top()            retorna los terminos mas frecuentes
TablaHashTerminos.mostrar_metricas()       muestra N, M, factor de carga y colisiones
```

### Usuarios sugeridos para la demo

Para mostrar que la Entrega II funciona, se pueden usar estos usuarios:

```text
spez
karmanaut
gallowboob
```

Los tres entregan contactos separados en 1°, 2° y 3° grado, sin repetir usuarios entre niveles.
