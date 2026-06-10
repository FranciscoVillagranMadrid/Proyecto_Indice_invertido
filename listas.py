# listas.py
#nodos y listas enlazadas hechas a mano.

#se crea el nodo de strings para almacenar en la lista enlazada de terminos
class NodoStr:
    def __init__(self, dato):
        self.dato = dato #tiene su propio dato
        self.siguiente = None #por ahora no apunta a nadie

#nodo que almacena cada post
class NodoPost:
    def __init__(self, post):
        self.post = post #almacena su propio post
        self.siguiente = None #por ahora no apunta a nadie

#nodo que almacena los usuarios a partir de su username
class NodoUsuario:
    def __init__(self, username):
        self.username = username #almacena el username del usuario
        self.siguiente = None #por ahora no apunta a nadie

#nodo que almacena los likes de un post
class NodoLike:
    def __init__(self, username):
        self.username = username #almacena el username o like simbólico
        self.siguiente = None #por ahora no apunta a nadie

#lista enlazada que almacena los terminos de un post (palabras clave)
#incluye funciones para recorrer y manipular la lista
class ListaTerminos:

    #se inicializa con tamaño 0
    def __init__(self):
        self.head = None
        self.tamaño = 0

    #inserta un valor al inicio de la lista enlazada
    def insertar(self, termino):
        
        if termino == "" or self.contiene(termino):#si el termino es "" o el termino ya esta en la lista no se agrega
            return
        
        nuevo = NodoStr(termino) #se crea un nodo con el termino
        nuevo.siguiente = self.head #nuevo nodo apunta al head de la lista
        self.head = nuevo #ahora el nuevo nodo queda como head
        self.tamaño = self.tamaño + 1 #se aumenta el tamaño de la lista

    #busca un termino dentro de la lista
    def contiene(self, termino):
        actual = self.head #variable de busqueda que empieza desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
         
            if actual.dato == termino:
                return True #retorna True en caso de que encuentre el termino que se busca
            actual = actual.siguiente
            
        return False #retorna False en caso de que no lo encuentre

    #función que recorre la lista desde el head y retorna los datos
    def recorrer(self):
        datos = [] #guarda temporalmente los datos de la lista
        actual = self.head #empieza desde el head
        
        while actual is not None: #recorre hasta que no queden nodos
            datos.append(actual.dato) #guarda en una lista los datos de cada nodo
            actual = actual.siguiente #avanza al siguiente nodo
        return datos

    #funcion que cuenta y retorna el tamaño de la lista
    def contar(self):
        return self.tamaño

#crea la lista enlazada que almacena los post
#incluye funciones para recorrer y manipular la lista
class ListaPosts:
    
    #se inicializa la lista con tamaño 0
    def __init__(self):
        self.head = None
        self.tamaño = 0

    #inserta los post al inicio de la lista enlazada
    def insertar(self, post):
        
        if post is None or self.contiene_id(post.post_id): #si el post es nulo o ya está su id dentro de la lista no se inserta
            return
        
        nuevo = NodoPost(post) #crea el nuevo nodo con el post
        nuevo.siguiente = self.head #el nodo nuevo apunta al head de la lista
        self.head = nuevo #ahora el nuevo nodo queda como head
        self.tamaño = self.tamaño + 1 #aumenta el tamaño de la lista

    #funcion que busca el id del post dentro de la lista
    def contiene_id(self, post_id): 
        actual = self.head #variable de busqueda que inicia desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            
            if actual.post.post_id == post_id: #si el id que se busca se encuentra en la lista retorna True
                return True
   
            actual = actual.siguiente #avanza al siguiente nodo
        return False #si no encuentra el id del post retorna False

    #funcion que recorre la lista
    def recorrer(self):
        datos = [] #guarda temporalmente los datos de la lista
        actual = self.head #crea la variable de busqueda que inicia desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            datos.append(actual.post) #guarda los post en la lista de datos creada previamente
            actual = actual.siguiente #avanza al siguiente nodo
        return datos #retorna la lista con los datos

    #funcion que muestra el tamaño de la lista 
    def contar(self):
        return self.tamaño #retorna el tamaño de la lista

#crea la lista enlazada que almacena los usuarios
#incluye funciones para recorrer y manipular la lista

class ListaUsuarios:
    #se inicializa la lista con tamaño 0
    def __init__(self):
        self.head = None
        self.tamaño = 0

    #inserta los username al inicio de la lista enlazada
    def insertar(self, username):
        
        if username == "" or self.contiene(username): #si el username es "" o la lista ya tiene el username no se agrega
            return
        
        nuevo = NodoUsuario(username) #crea un nodo con el username
        nuevo.siguiente = self.head #el nodo nuevo apunta al head de la lista 
        self.head = nuevo #ahora el nuevo nodo queda como head
        self.tamaño = self.tamaño + 1 #aumenta el tamaño de la lista

    #funcion que busca el username dentro de la lista
    def contiene(self, username): 
        actual = self.head #variable de busqueda que inicia desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            
            if actual.username == username: #si el username que busca se encuentra en la lista retorna True
                return True
            
            actual = actual.siguiente #avanza al siguiente nodo
        return False #si no encuentra el username retorna False

    #funcion que recorre la lista
    def recorrer(self):
        datos = [] #guarda temporalmente los datos de la lista
        actual = self.head #crea la variable de busqueda que inicia desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            datos.append(actual.username) #agrega los datos de la lista a la lista temporal que se creo previamente
            actual = actual.siguiente #avanza al siguiente nodo
        return datos #retorna la lista con los datos

    #funcion que muestra el tamaño de la lista
    def contar(self):
        return self.tamaño

#crea la lista enlazada que almacena los likes en los post
#incluye funciones para recorrer y manipular la lista
class ListaLikes:
    #el dataset solo trae un score total, no los usuarios reales que dieron like
    #por eso se limita la cantidad para no crear demasiados nodos
    MAX_LIKES = 30

    #se inicializa la lista con tamaño 0
    def __init__(self):
        self.head = None
        self.tamaño = 0

    #inserta los likes simbolicos al inicio de la lista enlazada
    def insertar(self, username):
        
        if username == "" or self.contiene(username): #si el username es "" o ya existe dentro de la lista no se agrega
            return
        
        if self.tamaño >= ListaLikes.MAX_LIKES: #si el tamaño de la lista llegó al límite no se agrega
            return
        
        nuevo = NodoLike(username) #crea el nodo nuevo
        nuevo.siguiente = self.head #el nodo nuevo apunta al head de la lista
        self.head = nuevo #ahora el nuevo nodo queda como head
        self.tamaño = self.tamaño + 1 #aumenta el tamaño de la lista

    #funcion que busca el username dentro de la lista
    def contiene(self, username):
        actual = self.head #variable de busqueda que inicia desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            
            if actual.username == username: #si el username que busca se encuentra en la lista retorna True
                return True
            
            actual = actual.siguiente #avanza al siguiente nodo
        return False #si no encuentra el username retorna False

    #funcion que recorre la lista
    def recorrer(self):
        datos = [] #guarda temporalmente los datos de la lista
        actual = self.head #variable de busqueda que empieza desde el head
        
        while actual is not None: #mientras queden nodos sigue el ciclo
            datos.append(actual.username) #agrega los datos de la lista a la lista temporal creada previamente
            actual = actual.siguiente #avanza al siguiente nodo
        return datos #retorna los datos

    #funcion que muestra el tamaño de la lista
    def contar(self):
        return self.tamaño
