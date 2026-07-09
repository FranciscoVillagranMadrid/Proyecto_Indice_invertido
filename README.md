# Sistema de Red Social con Índice Invertido, Grafo y Tabla Hash

Proyecto semestral de **ICI313 - Estructuras de Datos**.

El sistema procesa datos adaptados de Reddit/Pushshift y reúne las tres etapas del proyecto en una sola aplicación. La Entrega I proporciona los índices invertidos y las listas enlazadas base; la Entrega II incorpora un grafo no dirigido de contactos y un recorrido BFS por grados; la Entrega III agrega una tabla hash propia para contabilizar la frecuencia de los términos del dataset.

## Requisitos y ejecución

- Python 3.
- No se requieren bibliotecas externas.
- Los archivos CSV y `stopwords.txt` deben permanecer en la misma carpeta que el programa principal.

Para ejecutar:

```bash
python red_social.py
```

El programa carga los datos, construye los índices invertidos, genera el grafo, construye la tabla hash y habilita el menú de consultas.

## Archivos del proyecto

```text
listas.py                      Nodos y listas enlazadas propias.
indices.py                     Filtro de stopwords e índices invertidos.
grafo_contactos.py             Grafo no dirigido y recorrido BFS por niveles.
tabla_hash.py                  Tabla hash djb2 con encadenamiento separado.
red_social.py                  Entidades, carga de datos, integración y menú principal.
preprocesar_reddit.py          Preparación del dataset original de Reddit.
usuarios.csv                   Usuarios procesados.
posts.csv                      Publicaciones procesadas.
relaciones.csv                 Relaciones de contacto procesadas.
stopwords.txt                  Palabras excluidas durante la indexación.
red_social_presentacion_final.pptx  Presentación de las Entregas II y III.
```

## Flujo general del sistema

```text
Carga de stopwords
        ↓
Carga de usuarios, posts y relaciones
        ↓
Construcción de índices invertidos
        ↓
Construcción del grafo de contactos
        ↓
Construcción de la tabla hash de términos
        ↓
Consultas desde el menú principal
```

## Entrega I: estructuras base e índices invertidos

La Entrega I proporciona las listas enlazadas propias utilizadas en las etapas posteriores y dos índices principales:

```text
término  -> ListaPosts enlazada
usuario  -> ListaUsuarios enlazada de contactos
```

Los diccionarios se utilizan como mapas de acceso a las claves. Los valores asociados a cada clave son listas enlazadas implementadas en `listas.py`.

El filtro de stopwords normaliza los términos, elimina palabras comunes, descarta números aislados y omite palabras de longitud menor o igual a dos caracteres.

## Entrega II: grafo no dirigido y BFS

### Representación del grafo

El grafo se construye a partir del índice invertido de usuarios de la Entrega I. Cada vértice se identifica por su `username`, mantiene una referencia al objeto `Usuario` correspondiente y posee una lista enlazada de vecinos:

```text
username -> ListaUsuarios enlazada de contactos
```

Las relaciones son no dirigidas. Al agregar una conexión entre `A` y `B`, se registra `B` en la lista de `A` y `A` en la lista de `B`.

La implementación evita:

- bucles, rechazando relaciones donde `usuario == contacto`;
- aristas duplicadas, mediante la verificación previa de la lista enlazada;
- pérdida de simetría, mediante `validar_simetria()`.

### Recorrido por grados

`obtener_contactos_grado()` implementa BFS con control explícito de niveles. El recorrido utiliza una cola para el nivel actual, otra para el nivel siguiente y una estructura de visitados para impedir ciclos y repeticiones.

La función separa los resultados en:

```text
1° grado: contactos directos del usuario raíz.
2° grado: contactos nuevos descubiertos desde el primer nivel.
3° grado: contactos nuevos descubiertos desde el segundo nivel.
```

El usuario raíz se marca como visitado antes de iniciar el recorrido, por lo que no puede reaparecer en niveles posteriores. Cada usuario se incorpora una sola vez, en el primer nivel donde es descubierto.

### Complejidad

En el peor caso, el recorrido BFS tiene:

```text
Tiempo:  O(V + E)
Memoria: O(V)
```

`V` corresponde a los usuarios del grafo y `E` a las aristas. En esta implementación el recorrido se detiene al completar el tercer grado.

## Entrega III: tabla hash de frecuencia de términos

### Objetivo

La tabla hash registra la frecuencia total de cada término válido en todos los textos. Esta información es distinta de la almacenada en el índice invertido:

```text
Índice invertido: término -> posts donde aparece.
Tabla hash:        término -> cantidad total de apariciones.
```

El índice invertido entrega el tamaño del vocabulario único `N`. Posteriormente, la tabla hash vuelve a recorrer los textos para contabilizar todas las apariciones, incluidas las repeticiones dentro de un mismo post.

### Estructura

La tabla se implementa como un arreglo de `M` casillas. Cada casilla contiene una `ListaTerminosHash` enlazada propia:

```text
TablaHashTerminos
    -> arreglo de M casillas
        -> ListaTerminosHash
            -> NodoTerminoHash(termino, frecuencia, siguiente)
```

No se utiliza un `dict` de Python para reemplazar la tabla hash de frecuencia.

### Función hash djb2

`calcular_hash()` utiliza la función djb2:

```text
hash inicial = 5381
hash = hash * 33 + valor del carácter
```

En el código, la multiplicación por 33 se implementa como:

```python
(valor_hash << 5) + valor_hash
```

Después de procesar cada carácter, el valor se trunca a 32 bits:

```python
valor_hash &= 0xFFFFFFFF
```

Finalmente, el índice de la tabla se obtiene mediante:

```python
valor_hash % M
```

### Dimensionamiento

El tamaño de la tabla se calcula dinámicamente como el menor número primo que cumple:

```text
M >= 1.5 * N
```

Con los archivos incluidos:

```text
N = 304 términos únicos
1.5 * N = 456
M = 457, primer número primo mayor o igual a 456
Factor de carga α = N / M = 0.6652
```

### Resolución de colisiones

Las colisiones se resuelven mediante encadenamiento separado. Cuando dos términos distintos generan el mismo índice, ambos se almacenan como nodos diferentes dentro de la lista enlazada de esa casilla.

Si el término ya existe en la cadena, no se crea un nodo nuevo; se incrementa su frecuencia.

### Consulta Top-N

`obtener_top()` permite recuperar los términos de mayor frecuencia para valores de `N` iguales a 5, 10 y 20. La selección se realiza manualmente y, en caso de empate de frecuencia, se utiliza el orden alfabético para mantener una salida determinista.

### Métricas de la tabla

El programa reporta:

```text
N: cantidad de términos únicos.
M: cantidad de casillas de la tabla.
Factor de carga: N / M.
Total de colisiones.
Largo máximo de cadena.
Largo promedio de las cadenas no vacías.
```

Resultados obtenidos con el dataset incluido:

```text
N                              : 304
M                              : 457
Factor de carga                : 0.6652
Total de colisiones            : 91
Largo máximo de cadena         : 4
Promedio de cadenas no vacías  : 1.43
```

## Resultados del grafo con el dataset incluido

```text
Usuarios cargados              : 30
Posts cargados                 : 50
Entradas de contacto almacenadas: 64
Usuarios en el grafo           : 30
Aristas no dirigidas           : 32
```

Cada arista no dirigida se almacena en ambos sentidos en la lista de adyacencia. Por esta razón, 64 entradas dirigidas corresponden a 32 aristas no dirigidas.

## Funciones principales

### Grafo

```text
GrafoContactos.agregar_usuario()            registra un vértice y su referencia.
GrafoContactos.agregar_contacto()           agrega una arista en ambos sentidos.
GrafoContactos.construir_desde_indice()     construye el grafo desde la Entrega I.
GrafoContactos.obtener_contactos_grado()    ejecuta BFS hasta el grado solicitado.
GrafoContactos.validar_simetria()            verifica que cada relación sea bidireccional.
GrafoContactos.total_aristas()               cuenta cada arista no dirigida una sola vez.
```

### Tabla hash

```text
TablaHashTerminos.calcular_hash()            implementa djb2 y obtiene la casilla.
TablaHashTerminos.calcular_tamano()          calcula el primer primo válido para M.
TablaHashTerminos.construir()                procesa los posts y cuenta términos.
TablaHashTerminos.insertar()                 inserta o actualiza una frecuencia.
TablaHashTerminos.obtener_top()              obtiene los términos más frecuentes.
TablaHashTerminos.mostrar_metricas()         presenta las métricas de la tabla.
```

## Menú principal

```text
1. Buscar posts por término o palabra clave.
2. Buscar un usuario y mostrar sus contactos directos.
3. Mostrar algunos posts cargados.
4. Mostrar el resumen de estructuras y datos.
5. Consultar contactos de 1°, 2° y 3° grado mediante BFS.
6. Consultar Top-5, Top-10 o Top-20 términos.
7. Mostrar las métricas de la tabla hash.
8. Salir.
```

## Adaptación del dataset

Reddit no proporciona una lista de amigos equivalente a la de otras redes sociales. Por este motivo, las relaciones del proyecto se generan a partir de interacciones y co-participación de usuarios.

Reddit tampoco entrega la identidad individual de quienes realizaron cada voto. El atributo `score` se utiliza únicamente para generar likes simbólicos dentro del modelo de la Entrega I.

## Creación dinámica de estructuras

Los límites utilizados durante la carga controlan la cantidad de registros procesados, pero no convierten las estructuras en arreglos estáticos. Los nodos de las listas enlazadas, las listas de adyacencia y las cadenas de colisión se crean durante la ejecución.
