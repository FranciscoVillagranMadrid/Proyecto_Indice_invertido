# tabla_hash.py
# entrega 3: tabla hash propia para contar frecuencia de terminos
# usa djb2 y colisiones por encadenamiento separado con listas enlazadas propias

# nodo que guarda un termino y la cantidad de veces que aparece
class NodoTerminoHash:

    def __init__(self, termino):
        self.termino = termino #palabra guardada en la tabla
        self.frecuencia = 1 #parte en 1 porque el termino ya aparecio una vez
        self.siguiente = None #apunta al siguiente nodo de la cadena


# lista enlazada usada en cada posicion de la tabla hash
# sirve para resolver colisiones por encadenamiento separado
class ListaTerminosHash:

    def __init__(self):
        self.head = None #primer nodo de la cadena
        self.tamaño = 0 #cantidad de terminos distintos en esta cadena

    #busca un termino dentro de esta cadena
    def buscar(self, termino):
        actual = self.head #empieza desde el primer nodo

        while actual is not None: #recorre hasta que no queden nodos
            if actual.termino == termino: #si encuentra el termino retorna el nodo
                return actual
            actual = actual.siguiente #avanza al siguiente nodo

        return None #si no lo encuentra retorna None

    #inserta un termino o aumenta su frecuencia si ya estaba en la cadena
    def insertar(self, termino):
        nodo = self.buscar(termino) #primero revisa si el termino ya existe

        if nodo is not None: #si ya estaba, solo aumenta la frecuencia
            nodo.frecuencia = nodo.frecuencia + 1
            return False #False indica que no fue un termino nuevo

        nuevo = NodoTerminoHash(termino) #crea el nuevo nodo con el termino
        nuevo.siguiente = self.head #lo inserta al inicio de la cadena
        self.head = nuevo #actualiza el head
        self.tamaño = self.tamaño + 1 #aumenta el tamaño de esta cadena
        return True #True indica que se agrego un termino nuevo

    #recorre la cadena y devuelve sus nodos para poder mostrarlos o calcular top
    def recorrer(self):
        datos = [] #lista auxiliar solo para mostrar/procesar resultados
        actual = self.head #empieza desde el head

        while actual is not None: #recorre todos los nodos de la cadena
            datos.append(actual)
            actual = actual.siguiente

        return datos


# tabla hash principal para la frecuencia de terminos
class TablaHashTerminos:

    def __init__(self):
        self.tabla = None #arreglo donde cada posicion tiene una ListaTerminosHash
        self.tamano_tabla = 0 #M: tamaño de la tabla
        self.cantidad_terminos = 0 #N: cantidad de terminos unicos guardados

    #calcula el hash usando djb2
    def calcular_hash(self, termino):
        valor_hash = 5381 #valor inicial clasico de djb2
        i = 0 #indice para recorrer el termino

        while i < len(termino): #recorre caracter por caracter
            valor_hash = ((valor_hash << 5) + valor_hash) + ord(termino[i]) #hash * 33 + caracter
            valor_hash &= 0xFFFFFFFF #trunca a 32 bits como pide la pauta en Python
            i = i + 1

        return valor_hash % self.tamano_tabla #retorna la posicion dentro de la tabla

    #verifica si un numero es primo
    def es_primo(self, numero):
        if numero < 2:
            return False
        if numero == 2:
            return True
        if numero % 2 == 0:
            return False

        divisor = 3
        while divisor * divisor <= numero: #solo revisa divisores hasta la raiz
            if numero % divisor == 0:
                return False
            divisor = divisor + 2 #avanza de dos en dos porque ya reviso pares

        return True

    #calcula M como el primer primo que cumple M >= 1.5 * N
    def calcular_tamano(self, cantidad_unicos):
        minimo = (cantidad_unicos * 3 + 1) // 2 #redondeo hacia arriba de 1.5 * N

        if minimo < 7:
            minimo = 7 #minimo simple para no crear una tabla demasiado chica

        candidato = minimo
        while not self.es_primo(candidato): #busca el siguiente primo
            candidato = candidato + 1

        return candidato

    #crea la tabla con M posiciones, cada una con una lista enlazada vacia
    def inicializar_tabla(self, cantidad_unicos):
        self.tamano_tabla = self.calcular_tamano(cantidad_unicos)
        self.tabla = []
        i = 0

        while i < self.tamano_tabla: #crea cada cadena vacia de la tabla
            self.tabla.append(ListaTerminosHash())
            i = i + 1

    #inserta una palabra valida en la tabla hash
    def insertar(self, termino):
        if termino == "" or self.tabla is None: #si no hay termino o tabla, no hace nada
            return

        indice = self.calcular_hash(termino) #calcula en que posicion queda el termino
        es_nuevo = self.tabla[indice].insertar(termino) #inserta en la cadena correspondiente

        if es_nuevo: #si el termino no existia antes, aumenta N
            self.cantidad_terminos = self.cantidad_terminos + 1

    #procesa una palabra antes de insertarla en la tabla
    #a diferencia del indice invertido, aqui cuenta cada aparicion valida
    def insertar_si_valido(self, palabra, filtro):
        termino = filtro.limpiar_palabra(palabra) #limpia signos y pasa a minuscula

        if termino != "" and len(termino) > 2 and not termino.isdigit(): #evita vacios, numeros y palabras muy cortas
            if not filtro.es_stopword(termino): #si no es stopword se guarda en la tabla
                self.insertar(termino)

    #recorre el texto completo de un post para contar apariciones reales
    def contar_texto(self, texto, filtro):
        palabra = "" #palabra temporal que se va armando
        i = 0

        while i < len(texto): #recorre el texto caracter por caracter
            c = texto[i]

            if c.isalnum() or c == "_": #si sirve para una palabra, se acumula
                palabra = palabra + c
            else:
                self.insertar_si_valido(palabra, filtro) #cuando aparece un signo, revisa la palabra armada
                palabra = "" #reinicia para la siguiente palabra

            i = i + 1

        self.insertar_si_valido(palabra, filtro) #revisa la ultima palabra del texto

    #construye la tabla hash a partir de todos los posts
    #cantidad_unicos viene del vocabulario del indice invertido, asi no se usa dict para calcular N
    def construir(self, posts, filtro, cantidad_unicos):
        if cantidad_unicos <= 0:
            cantidad_unicos = 1 #evita tabla con tamaño cero si no hay terminos

        self.cantidad_terminos = 0 #reinicia N por si se reconstruye
        self.inicializar_tabla(cantidad_unicos) #crea la tabla con M primo

        for post_id in posts: #recorre todos los posts cargados
            self.contar_texto(posts[post_id].texto, filtro) #cuenta cada aparicion valida del texto

    #busca un termino y retorna su nodo
    def buscar(self, termino):
        if termino == "" or self.tabla is None:
            return None

        indice = self.calcular_hash(termino)
        return self.tabla[indice].buscar(termino)

    #retorna la frecuencia de un termino, o 0 si no esta
    def obtener_frecuencia(self, termino):
        nodo = self.buscar(termino)

        if nodo is not None:
            return nodo.frecuencia

        return 0

    #devuelve todos los nodos de la tabla en una lista auxiliar
    def obtener_todos(self):
        todos = [] #lista auxiliar para poder calcular top
        i = 0

        while i < self.tamano_tabla: #recorre cada posicion de la tabla
            nodos = self.tabla[i].recorrer()
            j = 0

            while j < len(nodos): #agrega los nodos de esa cadena
                todos.append(nodos[j])
                j = j + 1

            i = i + 1

        return todos

    #obtiene los N terminos con mayor frecuencia
    def obtener_top(self, cantidad):
        todos = self.obtener_todos() #obtiene todos los nodos de la tabla

        if len(todos) == 0:
            return []

        if cantidad > len(todos):
            cantidad = len(todos) #no puede mostrar mas terminos de los que existen

        resultado = []
        i = 0

        while i < cantidad:
            indice_mayor = 0 #guarda la posicion del termino con mayor frecuencia
            j = 1

            while j < len(todos): #busca el mayor en la lista que queda
                if todos[j].frecuencia > todos[indice_mayor].frecuencia:
                    indice_mayor = j
                j = j + 1

            resultado.append(todos[indice_mayor]) #agrega el mayor encontrado
            todos.pop(indice_mayor) #lo saca para no repetirlo
            i = i + 1

        return resultado

    #cuenta las colisiones de la tabla
    #si una cadena tiene 3 nodos, se cuentan 2 colisiones en esa posicion
    def contar_colisiones(self):
        colisiones = 0
        i = 0

        while i < self.tamano_tabla:
            if self.tabla[i].tamaño > 1:
                colisiones = colisiones + (self.tabla[i].tamaño - 1)
            i = i + 1

        return colisiones

    #calcula el largo de la cadena mas grande
    def largo_maximo_cadena(self):
        maximo = 0
        i = 0

        while i < self.tamano_tabla:
            largo = self.tabla[i].tamaño
            if largo > maximo:
                maximo = largo
            i = i + 1

        return maximo

    #calcula el promedio considerando solo cadenas no vacias
    def largo_promedio_cadenas(self):
        total = 0
        no_vacias = 0
        i = 0

        while i < self.tamano_tabla:
            largo = self.tabla[i].tamaño
            if largo > 0:
                total = total + largo
                no_vacias = no_vacias + 1
            i = i + 1

        if no_vacias == 0:
            return 0.0

        return round(total / no_vacias, 2)

    #muestra las metricas pedidas para la tabla hash
    def mostrar_metricas(self):
        if self.tabla is None:
            print("La tabla hash no ha sido construida todavia.")
            return

        factor_carga = round(self.cantidad_terminos / self.tamano_tabla, 4)

        print("\nMetricas de la tabla hash:")
        print("  N (terminos unicos)       :", self.cantidad_terminos)
        print("  M (tamaño de la tabla)    :", self.tamano_tabla)
        print("  Factor de carga (N/M)     :", factor_carga)
        print("  Total de colisiones       :", self.contar_colisiones())
        print("  Largo maximo de cadena    :", self.largo_maximo_cadena())
        print("  Promedio cadenas no vacias:", self.largo_promedio_cadenas())
