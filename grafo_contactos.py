# grafo_contactos.py
# entrega 2: grafo no dirigido de contactos usando listas de adyacencia

# importa la lista enlazada de usuarios para armar las listas de adyacencia
from listas import ListaUsuarios

# clase que representa el grafo no dirigido de contactos
# cada nodo es un usuario y cada arista es una relacion entre dos usuarios
class GrafoContactos:

    # inicializa el grafo con un diccionario vacio de adyacencia
    def __init__(self):
        self.adyacencia = {}  # username -> ListaUsuarios con sus vecinos
        self.referencias_usuarios = {}  # username -> objeto Usuario del sistema

    # registra un usuario en el grafo si todavia no existe
    # referencia permite guardar el objeto Usuario asociado al vertice
    def agregar_usuario(self, usuario, referencia=None):
        if usuario != "" and usuario not in self.adyacencia:
            self.adyacencia[usuario] = ListaUsuarios()  # lista vacia de vecinos

        if usuario != "" and referencia is not None:
            self.referencias_usuarios[usuario] = referencia

    # retorna la referencia al objeto Usuario si fue registrada
    def obtener_referencia_usuario(self, usuario):
        if usuario in self.referencias_usuarios:
            return self.referencias_usuarios[usuario]
        return None

    # agrega una arista entre dos usuarios en ambos sentidos
    # si la arista ya existe, ListaUsuarios.insertar la ignora automaticamente
    def agregar_contacto(self, usuario, contacto):
        if usuario == "" or contacto == "" or usuario == contacto:
            return  # no se agregan bucles ni datos vacios

        self.agregar_usuario(usuario)
        self.agregar_usuario(contacto)

        # grafo no dirigido: la arista va en los dos sentidos
        self.adyacencia[usuario].insertar(contacto)
        self.adyacencia[contacto].insertar(usuario)

    # construye el grafo leyendo el indice invertido de usuarios ya cargado
    # no vuelve a leer el csv, solo usa lo que ya esta en memoria
    def construir_desde_indice(self, indice_usuarios):
        for username in indice_usuarios.mapa:  # recorre todos los usuarios del indice
            self.agregar_usuario(username)  # registra el usuario en el grafo

            lista_contactos = indice_usuarios.obtener_contactos(username)  # obtiene sus contactos

            if lista_contactos is not None:
                contactos = lista_contactos.recorrer()  # los convierte a lista para recorrer
                i = 0
                while i < len(contactos):
                    self.agregar_contacto(username, contactos[i])  # agrega la arista (bidireccional)
                    i = i + 1

    # realiza el BFS desde un usuario raiz y devuelve contactos por nivel
    # retorna una lista de listas: [[grado1], [grado2], [grado3]]
    # siempre devuelve exactamente 'grados' sublistas aunque algunas esten vacias
    def obtener_contactos_grado(self, usuario_raiz, grados):
        if usuario_raiz not in self.adyacencia:
            return None  # el usuario no existe en el grafo

        visitados = {}  # guarda los usuarios ya procesados para no repetirlos
        visitados[usuario_raiz] = True  # marca la raiz como visitada desde el inicio

        cola = [usuario_raiz]  # cola del BFS, empieza solo con la raiz
        resultado = []  # lista donde se guardan los contactos de cada grado
        nivel_actual = 0

        while nivel_actual < grados and len(cola) > 0:
            siguiente_cola = []   # usuarios que se van a procesar en el siguiente nivel
            nivel_contactos = []  # contactos nuevos encontrados en este nivel

            i = 0
            while i < len(cola):
                actual = cola[i]
                vecinos = self.adyacencia[actual].recorrer()  # obtiene los vecinos del nodo actual

                j = 0
                while j < len(vecinos):
                    vecino = vecinos[j]
                    if vecino not in visitados:  # si el vecino aun no fue visitado
                        visitados[vecino] = True  # lo marca como visitado
                        nivel_contactos.append(vecino)  # lo agrega al nivel actual
                        siguiente_cola.append(vecino)  # lo encola para el siguiente nivel
                    j = j + 1

                i = i + 1

            resultado.append(nivel_contactos)  # guarda los contactos de este grado (puede estar vacio)
            cola = siguiente_cola  # avanza a los nodos del siguiente nivel
            nivel_actual = nivel_actual + 1

        # rellena con listas vacias si el BFS termino antes de alcanzar todos los grados
        while len(resultado) < grados:
            resultado.append([])

        # se ordena cada nivel solo para mostrar/defender mejor la salida
        # la estructura del grafo sigue siendo lista enlazada de adyacencia
        i = 0
        while i < len(resultado):
            resultado[i].sort()
            i = i + 1

        return resultado

    # revisa que por cada A -> B tambien exista B -> A
    # sirve para demostrar que el grafo quedo realmente no dirigido
    def validar_simetria(self):
        for usuario in self.adyacencia:
            vecinos = self.adyacencia[usuario].recorrer()
            i = 0

            while i < len(vecinos):
                vecino = vecinos[i]

                if vecino not in self.adyacencia:
                    return False

                if not self.adyacencia[vecino].contiene(usuario):
                    return False

                i = i + 1

        return True

    # muestra en pantalla los contactos por grado de un usuario
    def mostrar_contactos_grado(self, usuario_raiz, grados):
        if usuario_raiz not in self.adyacencia:
            print("Usuario no encontrado en el grafo:", usuario_raiz)
            return

        resultado = self.obtener_contactos_grado(usuario_raiz, grados)

        if resultado is None:
            print("Usuario no encontrado:", usuario_raiz)
            return

        print("\nContactos por grado para el usuario:", usuario_raiz)

        i = 0
        while i < len(resultado):
            grado = i + 1
            contactos = resultado[i]
            print("\nGrado " + str(grado) + " (" + str(len(contactos)) + " contacto(s)):")

            if len(contactos) == 0:
                print("  (sin contactos en este grado)")
            else:
                j = 0
                while j < len(contactos) and j < 15:  # muestra maximo 15 por grado
                    print("  -", contactos[j])
                    j = j + 1

                if len(contactos) > 15:
                    print("  ... y", len(contactos) - 15, "contacto(s) mas en este grado")

            i = i + 1

    # retorna la cantidad de usuarios registrados en el grafo
    def total_usuarios(self):
        return len(self.adyacencia)

    # retorna la cantidad de aristas del grafo
    # como cada arista se guarda en dos listas, se divide entre 2
    def total_aristas(self):
        total = 0
        for usuario in self.adyacencia:
            total = total + self.adyacencia[usuario].contar()
        return total // 2
