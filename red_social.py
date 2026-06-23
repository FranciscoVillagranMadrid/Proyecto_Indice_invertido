# red_social.py

#importa las listas y los indices invertidos ya creados
from listas import ListaUsuarios, ListaLikes, ListaTerminos
from indices import FiltroStopwords, IndiceInvertidoPosts, IndiceInvertidoUsuarios
from grafo_contactos import GrafoContactos      #entrega 2: grafo de contactos
from tabla_hash import TablaHashTerminos        #entrega 3: tabla hash de terminos

#separador de los archivos csv
SEPARADOR = "|"

#crea un usuario con todos sus atributos
class Usuario:
    def __init__(self, user_id, username, karma): #almacena los datos del usuario(id,username,karma) 
        self.user_id = user_id
        self.username = username
        self.karma = karma
        self.contactos = ListaUsuarios() #lista enlazada donde se guardan los contactos del usuario

    #funcion que retorna como se vera el usuario al mostrarlo
    def __repr__(self):
        return "Usuario(" + self.username + ", karma=" + str(self.karma) + ")"

#crea los post con todos sus atributos
class Post:
    def __init__(self, post_id, username, texto, score): #almacena los datos del post (id,username,texto,score)
        self.post_id = post_id
        self.username = username
        self.texto = texto
        self.score = score
        self.terminos = ListaTerminos() #lista enlazada donde se guardan los terminos del post
        self.likes = ListaLikes() #lista enlazada donde se guardan los likes del post
        self.cargar_likes_simbolicos() #crea los likes simbolicos del post a partir del score 

    #funcion que transforma el score en likes simbolicos (reddit no usa sistema de likes puro)
    #reddit entrega el score total, pero no dice que usuario votó
    def cargar_likes_simbolicos(self): 
        cantidad = self.score #toma el score del post como base para crear likes simbolicos
        if cantidad < 0: #si el score es negativo no crea likes
            cantidad = 0
        if cantidad > ListaLikes.MAX_LIKES: #si la cantidad de likes es mayor al maximo de likes de la lista enlazada (30)
            cantidad = ListaLikes.MAX_LIKES #los limita al maximo de la lista enlazada (30)
        i = 1 #contador para crear los likes simbolicos
        while i <= cantidad: #mientras la variable no sea mayor a la cantidad de likes sigue el ciclo
            self.likes.insertar("like_" + str(i)) #inserta cada like simbolico en la lista enlazada
            i = i + 1 #sigue al siguiente like

    #funcion que retorna como se verá el post al mostrarlo
    def __repr__(self):
        texto = self.texto #toma el texto del post
        if len(texto) > 45: #si el texto tiene mas de 45 caracteres, lo corta y agrega "..."
            texto = texto[:45] + "..."
        return "Post(" + self.post_id + ", @" + self.username + ", score/likes_simbolicos=" + str(self.score) + ", '" + texto + "')"

#clase principal que maneja la red social
class SistemaRedSocial:
    def __init__(self):
        self.usuarios = {} #diccionario para guardar usuarios
        self.posts = {} #diccionario para guardar posts
        self.filtro = FiltroStopwords() #filtro para guardar y revisar stopwords
        self.indice_posts = IndiceInvertidoPosts() #indice invertido para los post
        self.indice_usuarios = IndiceInvertidoUsuarios() #indice invertido para los usuarios
        self.total_relaciones = 0 #cantidad total de relaciones cargadas en los archivos
        self.grafo = GrafoContactos() #grafo de contactos para la entrega 2
        self.tabla_hash = TablaHashTerminos() #tabla hash de terminos para la entrega 3

    #funcion que transforma texto a numeros para leer los archivos csv
    def numero(self, texto):
        texto = texto.strip() #borra los espacios en blanco del texto
        if texto == "": #si no existe retorna 0
            return 0
        try: 
            return int(texto) #intenta convertir el texto en numero entero
        except ValueError: #en caso de que sea otro valor da error de formato (ValueError)
            return 0 #retorna 0

    #funcion que lee el archivo de stopwords y las guarda en el filtro
    def cargar_stopwords(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8") #abre el archivo codigficado en utf-8 para su lectura (como texto)
        linea = archivo.readline() #lee la primera linea del archivo
        while linea != "": #mientras no llegue al final del archivo sigue el ciclo
            palabra = linea.strip().lower() #pasa el texto a minuscula y borra los espacios en blanco
            if palabra != "" and not palabra.startswith("#"): #si la palabra existe y no empieza por "#" 
                self.filtro.agregar(palabra) #la agrega al filtro de stopwords
            linea = archivo.readline() #lee la siguiente linea del archivo
        archivo.close() #cierra el archivo

    #funcion que lee el archivo de usuarios
    #el karma es una medida de reputacion del usuario en reddit 
    def cargar_usuarios(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8") #abre el archivo en codificación utf-8 para su lectura (como texto)
        archivo.readline() #lee la primera linea del archivo (no importa guardarla ya que es el encabezado)
        linea = archivo.readline() #lee la primera linea de datos del usuario
        while linea != "": #mientras no llegue al final del archivo sigue el ciclo
            linea = linea.strip() #borra los espacios en blanco de cada linea
            if linea != "": #si la linea no esta vacia
                partes = linea.split(SEPARADOR) #crea partes con el separador
                if len(partes) >= 3: #si hay 3 partes o más en una linea almacena
                    user_id = partes[0].strip() #parte 1 para el id 
                    username = partes[1].strip() #parte 2 para el username
                    karma = self.numero(partes[2]) #parte 3 para el karma del usuario
                    if username != "" and username not in self.usuarios: #si el username no esta vacio y no esta registrado
                        self.usuarios[username] = Usuario(user_id, username, karma) #lo agrega con su id, username y su karma
                        self.indice_usuarios.registrar_usuario(username) #registra el usuario en el indice invertido
            linea = archivo.readline() #lee la siguiente linea del archivo
        archivo.close() #cierra el archivo

    #funcion que lee el archivo de los posts
    #el score es el puntaje del post y luego se usa para crear likes simbolicos
    def cargar_posts(self, ruta): 
        archivo = open(ruta, "r", encoding="utf-8") #abre el archivo en codificación utf-8 para su lectura (como texto)
        archivo.readline() #lee la primera linea del archivo (no importa guardarla ya que es el encabezado)
        linea = archivo.readline() #lee la primera linea de datos de los post
        while linea != "": #mientras no llegue al final del archivo sigue el ciclo
            linea = linea.strip() #borra los espacios en blanco de cada linea
            if linea != "": #si la linea no esta vacia 
                partes = linea.split(SEPARADOR) #crea partes con el separador 
                if len(partes) >= 4: #si hay 4 partes o más en una linea almacena 
                    post_id = partes[0].strip() #parte 1 para el id
                    username = partes[1].strip() #parte 2 para el username
                    texto = partes[2].strip() #parte 3 para el texto del post
                    score = self.numero(partes[3]) #parte 4 para el score de post

                    if post_id != "" and username != "" and texto != "" and post_id not in self.posts: #si el post tiene datos validos pero no está guardado
                        if username not in self.usuarios: #si el usuario no esta registrado en el diccionario de usuarios
                            self.usuarios[username] = Usuario("unknown_"+username, username, 0) #crea un usuario temporal porque no venia en usuarios.csv
                            self.indice_usuarios.registrar_usuario(username) #registra el usuario en el indice invertido
                        self.posts[post_id] = Post(post_id, username, texto, score) #registra el post con su id, el username asociado, texto y score
            linea = archivo.readline() #lee la siguiente linea del archivo
        archivo.close() #cierra el archivo

    #funcion que lee el archivo de relaciones entre usuarios
    #como la pauta habla de amigos/contactos, las relaciones se guardan en ambos sentidos
    #reddit no usa amigos como tal, pero aqui las interacciones se adaptan como contactos mutuos
    def cargar_relaciones(self, ruta):
        archivo = open(ruta, "r", encoding="utf-8") #abre el archivo en codificacion utf-8 para su lectura
        archivo.readline() #lee la primera linea del archivo, no se guarda porque es el encabezado
        linea = archivo.readline() #lee la primera linea de datos de las relaciones

        while linea != "": #mientras no llegue al final del archivo sigue el ciclo
            linea = linea.strip() #borra los espacios en blanco de cada linea

            if linea != "": #si la linea no esta vacia
                partes = linea.split(SEPARADOR) #crea partes usando el separador

                if len(partes) >= 2: #si hay 2 partes o mas, puede obtener origen y contacto
                    origen = partes[0].strip() #parte 1 para el usuario origen
                    contacto = partes[1].strip() #parte 2 para el usuario contacto

                    if origen != "" and contacto != "" and origen != contacto: #si origen y contacto tienen datos y no son el mismo usuario
                        if origen not in self.usuarios: #si el usuario origen no esta registrado en el diccionario de usuarios
                            self.usuarios[origen] = Usuario("unknown_" + origen, origen, 0) #crea un usuario temporal porque no venia en usuarios.csv
                            self.indice_usuarios.registrar_usuario(origen) #registra el usuario en el indice invertido

                        if contacto not in self.usuarios: #si el usuario contacto no esta registrado en el diccionario de usuarios
                            self.usuarios[contacto] = Usuario("unknown_" + contacto, contacto, 0) #crea un usuario temporal porque no venia en usuarios.csv
                            self.indice_usuarios.registrar_usuario(contacto) #registra el usuario en el indice invertido

                        #agrega la relacion desde origen hacia contacto
                        antes = self.usuarios[origen].contactos.contar() #cuenta cuantos contactos tenia el origen antes de insertar
                        self.usuarios[origen].contactos.insertar(contacto) #agrega el contacto a la lista enlazada del usuario origen
                        self.indice_usuarios.agregar_contacto(origen, contacto) #agrega la relacion al indice invertido de usuarios
                        despues = self.usuarios[origen].contactos.contar() #cuenta cuantos contactos tiene despues de insertar

                        if despues > antes: #si la cantidad aumento significa que se agrego una relacion nueva
                            self.total_relaciones = self.total_relaciones + 1 #aumenta el total de relaciones cargadas

                        #agrega la relacion inversa desde contacto hacia origen
                        antes = self.usuarios[contacto].contactos.contar() #cuenta cuantos contactos tenia el contacto antes de insertar
                        self.usuarios[contacto].contactos.insertar(origen) #agrega el origen como contacto del otro usuario
                        self.indice_usuarios.agregar_contacto(contacto, origen) #agrega la relacion inversa al indice invertido de usuarios
                        despues = self.usuarios[contacto].contactos.contar() #cuenta cuantos contactos tiene despues de insertar

                        if despues > antes: #si la cantidad aumento significa que se agrego la relacion inversa
                            self.total_relaciones = self.total_relaciones + 1 #aumenta el total de relaciones cargadas

            linea = archivo.readline() #lee la siguiente linea del archivo

        archivo.close() #cierra el archivo

    #funcion que construye el indice invertido de los post
    def construir_indices(self):
        self.indice_posts.construir(self.posts, self.filtro) #construye el indice usando los posts guardados y el filtro de stopwords

    #construye el grafo de contactos a partir del indice de usuarios ya cargado
    def construir_grafo(self):
        #primero registra cada vertice con referencia al objeto Usuario del sistema
        for username in self.usuarios:
            self.grafo.agregar_usuario(username, self.usuarios[username])

        #despues agrega las aristas usando el indice invertido de usuarios
        self.grafo.construir_desde_indice(self.indice_usuarios)

    #construye la tabla hash de frecuencia de terminos
    #depende de que construir_indices() haya sido llamado primero
    def construir_tabla_hash(self):
        cantidad_unicos = self.indice_posts.total_terminos() #N sale del vocabulario ya creado en el indice
        self.tabla_hash.construir(self.posts, self.filtro, cantidad_unicos) #cuenta las apariciones reales en los textos

    #funcion que busca post a través del termino
    def buscar_posts(self, termino):
        termino = self.filtro.limpiar_palabra(termino) #limpia el termino ingresado para buscarlo en el indice
        if termino == "" or self.filtro.es_stopword(termino): #si el termino esta vacio o es una stopword
            return [] #retorna una lista vacia porque no hay resultados validos
        lista = self.indice_posts.buscar(termino) #busca en el indice invertido de posts la lista enlazada asociada al termino
        if lista is None: #si no existe una lista de posts para ese termino
            return [] #retorna una lista vacia porque el termino no tiene posts asociados
        return lista.recorrer() #retorna los posts asociados recorriendo la lista enlazada

    #funcion que busca los contactos de un usuario
    def buscar_contactos(self, username):
        lista = self.indice_usuarios.obtener_contactos(username) #obtiene la lista enlazada de contactos asociada a ese usuario
        if lista is None: #si no existe una lista de contactos para ese usuario
            return [] #retorna una lista vacia porque el usuario no tiene contactos registrados
        return lista.recorrer() #retorna los contactos asociados recorriendo la lista enlazada

    #funcion que muestra el resumen de los datos cargados e indexados
    def mostrar_resumen(self):
        print("Usuarios cargados          :", len(self.usuarios))
        print("Posts cargados             :", len(self.posts))
        print("Relaciones cargadas        :", self.total_relaciones)
        print("Stopwords cargadas         :", self.filtro.total())
        print("Terminos indexados         :", self.indice_posts.total_terminos())
        print("Usuarios en el grafo       :", self.grafo.total_usuarios())
        print("Aristas del grafo          :", self.grafo.total_aristas())
        if self.grafo.validar_simetria():
            print("Grafo no dirigido          : OK, relaciones simetricas")
        else:
            print("Grafo no dirigido          : Revisar simetria")
        print("Terminos en tabla hash     :", self.tabla_hash.cantidad_terminos)
        if self.tabla_hash.tabla is not None:
            factor = round(self.tabla_hash.cantidad_terminos / self.tabla_hash.tamano_tabla, 4)
            print("M tabla hash               :", self.tabla_hash.tamano_tabla)
            print("Factor de carga hash       :", factor)
            print("Colisiones hash            :", self.tabla_hash.contar_colisiones())
            print("Largo maximo cadena hash   :", self.tabla_hash.largo_maximo_cadena())

#funcion que muestra los posts encontrados hasta un maximo
def mostrar_posts(posts, maximo):
    if len(posts) == 0: #si la cantidad de post es 0
        print("No se encontraron posts.")  
        return #termina la funcion
    i = 0 #indice para recorrer los post
    while i < len(posts) and i < maximo: #mientras queden post y no supere el maximo sigue el ciclo
        print("-", posts[i]) #muestra en pantalla el post 
        i = i + 1 #avanza al siguiente post

#funcion que muestra los contactos de un usuario hasta un maximo
def mostrar_contactos(contactos, maximo):
    if len(contactos) == 0: #si la cantidad de contactos es 0
        print("No se encontraron contactos.") 
        return #termina la funcion
    i = 0 #indice para recorrer los contactos
    while i < len(contactos) and i < maximo: #mientras queden contactos y no supere el maximo sigue el ciclo
        print("-", contactos[i]) #muestra en pantalla los contactos
        i = i + 1 #avanza al siguiente contacto

#funcion que muestra algunos posts cargados en el sistema
#esto sirve para comprobar que los posts si estan cargados aunque se busquen por terminos
def mostrar_posts_cargados(sistema, maximo):
    if len(sistema.posts) == 0: #si no hay posts cargados no muestra nada
        print("No hay posts cargados.")
        return

    print("\nAlgunos posts cargados:")
    contador = 0 #contador para no mostrar demasiados posts en pantalla

    for post_id in sistema.posts: #recorre los posts guardados en el diccionario
        if contador >= maximo: #si ya mostro el maximo se detiene
            break

        print("-", sistema.posts[post_id]) #muestra el post usando el __repr__ de la clase Post
        contador = contador + 1 #aumenta el contador para seguir con el siguiente post


#funcion main que llama a todo el proyecto
def main():
    sistema = SistemaRedSocial() #sistema es la red social completa

    #carga todos los archivos necesarios para armar la red social
    sistema.cargar_stopwords("stopwords.txt") #carga las stopwords desde el txt
    sistema.cargar_usuarios("usuarios.csv") #carga los usuarios desde el csv
    sistema.cargar_posts("posts.csv") #carga los posts desde el csv
    sistema.cargar_relaciones("relaciones.csv") #carga las relaciones entre usuarios
    sistema.construir_indices()      #construye el indice invertido de los posts
    sistema.construir_grafo()        #construye el grafo de contactos (entrega 2)
    sistema.construir_tabla_hash()   #construye la tabla hash de terminos (entrega 3)

    print("\nResumen de carga inicial")
    sistema.mostrar_resumen() #muestra el resumen inicial para comprobar que todo se cargo bien

    while True: #el menu sigue activo hasta que el usuario elija salir con la opcion 8
        print("\n===== RED SOCIAL - INDICE, GRAFO Y HASH =====")
        print("1. Buscar posts por termino / palabra clave")
        print("2. Buscar usuario y mostrar contactos directos")
        print("3. Mostrar algunos posts cargados")
        print("4. Mostrar resumen de carga")
        print("5. Buscar contactos por grado (BFS)")
        print("6. Mostrar Top-N terminos frecuentes")
        print("7. Mostrar metricas de tabla hash")
        print("8. Salir")

        opcion = input("Seleccione una opcion: ").strip() #lee la opcion elegida por el usuario

        if opcion == "1":
            #busca posts usando el indice invertido de terminos
            termino = input("Ingrese un termino o escriba TERMINOS para ver el indice de posts: ").strip()

            if termino.upper() == "TERMINOS": #si el usuario escribe TERMINOS se muestran algunos terminos del indice
                print("\nTerminos del indice invertido de posts:")
                contador = 0 #contador para no llenar la pantalla con todos los terminos

                for termino_indice in sistema.indice_posts.vocabulario: #recorre los terminos guardados en el indice
                    print("-", termino_indice) #muestra el termino
                    contador = contador + 1 #aumenta el contador

                    if contador >= 30: #muestra solo algunos terminos para que no sea tan largo
                        print("... se muestran solo algunos terminos.")
                        break

            else:
                posts = sistema.buscar_posts(termino) #busca los posts relacionados al termino ingresado

                if len(posts) == 0: #si no encuentra posts no termina el programa, solo avisa
                    print("No existen posts asociados al termino:", termino)
                else:
                    print("\nPosts encontrados para el termino:", termino)
                    mostrar_posts(posts, 5) #muestra hasta 5 posts encontrados

        elif opcion == "2":
            #busca los contactos asociados a un usuario usando el indice de usuarios
            usuario = input("Ingrese un username o escriba USUARIOS para ver el indice de usuarios: ").strip()

            if usuario.upper() == "USUARIOS": #si escribe USUARIOS muestra algunos usuarios cargados en el indice
                print("\nUsuarios del indice invertido de usuarios:")
                contador = 0 #contador para no mostrar demasiados usuarios

                for username in sistema.indice_usuarios.mapa: #recorre los usuarios guardados en el indice
                    print("-", username) #muestra el username
                    contador = contador + 1 #aumenta el contador

                    if contador >= 30: #limita la muestra para que no se llene la pantalla
                        print("... se muestran solo algunos usuarios.")
                        break

            else:
                contactos = sistema.buscar_contactos(usuario) #busca los contactos del usuario ingresado

                if len(contactos) == 0: #si no encuentra contactos no termina el programa, solo avisa
                    print("No se encontraron contactos para el usuario:", usuario)
                else:
                    print("\nContactos del usuario:", usuario)
                    mostrar_contactos(contactos, 8) #muestra hasta 8 contactos encontrados

        elif opcion == "3":
            #muestra algunos posts para demostrar que los posts estan cargados en memoria
            mostrar_posts_cargados(sistema, 8)

        elif opcion == "4":
            #muestra las cantidades cargadas y los terminos indexados
            print("\nResumen de carga")
            sistema.mostrar_resumen()

        elif opcion == "5":
            #busca contactos de un usuario por grado (1°, 2° y 3°) usando BFS
            usuario_raiz = input("Ingrese el username para buscar por grados: ").strip()

            if usuario_raiz == "":
                print("Debe ingresar un username.")
            else:
                sistema.grafo.mostrar_contactos_grado(usuario_raiz, 3)

        elif opcion == "6":
            #muestra los terminos mas frecuentes usando la tabla hash
            print("Seleccione la cantidad de terminos a mostrar: 5, 10 o 20")
            sub = input("Cantidad: ").strip()

            if sub not in ("5", "10", "20"):
                print("Opcion no valida. Ingrese 5, 10 o 20.")
            else:
                n = int(sub)
                top = sistema.tabla_hash.obtener_top(n)

                if len(top) == 0:
                    print("No hay terminos en la tabla hash.")
                else:
                    print("\nTop " + str(n) + " terminos mas frecuentes:")
                    i = 0
                    while i < len(top):
                        print(str(i + 1) + ". " + top[i].termino + "  (frecuencia: " + str(top[i].frecuencia) + ")")
                        i = i + 1

        elif opcion == "7":
            #muestra N, M, factor de carga, colisiones y largo de cadenas
            sistema.tabla_hash.mostrar_metricas()

        elif opcion == "8":
            break  #sale del while True para terminar el programa

        else:
            print("Opcion no valida. Intente nuevamente.")


#funcion para ejecutar el main 
if __name__ == "__main__":
    main()
