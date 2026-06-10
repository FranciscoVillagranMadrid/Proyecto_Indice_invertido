import os, sys, subprocess
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
from red_social import SistemaRedSocial
from grafo_contactos import GrafoContactos
from tabla_hash import TablaHashTerminos
from indices import FiltroStopwords

resultados=[]
def ok(nombre, cond, detalle=''):
    resultados.append((nombre, bool(cond), detalle))

# Carga conjunta del sistema
s=SistemaRedSocial()
s.cargar_stopwords('stopwords.txt')
s.cargar_usuarios('usuarios.csv')
s.cargar_posts('posts.csv')
s.cargar_relaciones('relaciones.csv')
s.construir_indices()
s.construir_grafo()
s.construir_tabla_hash()

ok('Carga usuarios', len(s.usuarios)==30, len(s.usuarios))
ok('Carga posts', len(s.posts)==50, len(s.posts))
ok('Carga relaciones', s.total_relaciones==64, s.total_relaciones)
ok('Carga stopwords', s.filtro.total()==111, s.filtro.total())
ok('Indice terminos', s.indice_posts.total_terminos()==304, s.indice_posts.total_terminos())
ok('Grafo usuarios', s.grafo.total_usuarios()==30, s.grafo.total_usuarios())
ok('Tabla hash terminos unicos', s.tabla_hash.cantidad_terminos==304, s.tabla_hash.cantidad_terminos)
ok('Tabla hash M primo >= 1.5N', s.tabla_hash.es_primo(s.tabla_hash.tamano_tabla) and s.tabla_hash.tamano_tabla >= 1.5*s.tabla_hash.cantidad_terminos, (s.tabla_hash.tamano_tabla, s.tabla_hash.cantidad_terminos))

# Entrega 1
posts_python=s.buscar_posts('python')
ok('Buscar termino python', len(posts_python)>0, len(posts_python))
ok('Stopword no devuelve resultados', s.buscar_posts('the')==[], s.buscar_posts('the'))
ok('Termino falso no se cae', s.buscar_posts('termino_fake_123')==[], s.buscar_posts('termino_fake_123'))
contactos_spez=s.buscar_contactos('spez')
ok('Buscar contactos spez', len(contactos_spez)>0, len(contactos_spez))
ok('Usuario falso no se cae', s.buscar_contactos('usuario_fake')==[], s.buscar_contactos('usuario_fake'))

# Entrega 2 real
for usuario in ['spez','karmanaut','gallowboob']:
    grados=s.grafo.obtener_contactos_grado(usuario,3)
    plano=[]
    if grados is not None:
        for nivel in grados:
            plano += nivel
    ok(f'BFS {usuario} retorna 3 niveles', grados is not None and len(grados)==3, grados)
    ok(f'BFS {usuario} sin raiz', usuario not in plano, plano)
    ok(f'BFS {usuario} sin duplicados', len(plano)==len(set(plano)), plano)
ok('BFS usuario inexistente retorna None', s.grafo.obtener_contactos_grado('usuario_fake',3) is None, '')

# Grafo aislado
g=GrafoContactos()
g.agregar_contacto('A','B')
g.agregar_contacto('B','C')
g.agregar_contacto('C','D')
g.agregar_contacto('A','B')
g.agregar_contacto('A','A')
res=g.obtener_contactos_grado('A',3)
ok('Grafo aislado grados correctos', res==[['B'],['C'],['D']], res)
ok('Grafo aislado sin duplicar aristas', g.total_aristas()==3, g.total_aristas())

# Entrega 3 aislada con apariciones reales
f=FiltroStopwords()
f.agregar('the')
class P:
    def __init__(self,texto): self.texto=texto
posts={'1':P('python python datos the 123 aa'), '2':P('datos python codigo codigo')}
t=TablaHashTerminos()
t.construir(posts, f, 3)
ok('Hash aislado frecuencia python 3', t.obtener_frecuencia('python')==3, t.obtener_frecuencia('python'))
ok('Hash aislado frecuencia datos 2', t.obtener_frecuencia('datos')==2, t.obtener_frecuencia('datos'))
ok('Hash aislado ignora stopword', t.obtener_frecuencia('the')==0, t.obtener_frecuencia('the'))
ok('Hash aislado M cumple techo', t.tamano_tabla >= 1.5*t.cantidad_terminos and t.es_primo(t.tamano_tabla), (t.tamano_tabla,t.cantidad_terminos))
ok('Hash top retorna orden', [n.termino for n in t.obtener_top(2)][0]=='python', [(n.termino,n.frecuencia) for n in t.obtener_top(2)])

# Menu integrado rápido por subprocess
entrada='4\n3\n1\npython\n2\nspez\n5\nspez\n6\n5\n7\n8\n'
proc=subprocess.run([sys.executable,'red_social.py'],input=entrada,text=True,capture_output=True,timeout=10,cwd=BASE_DIR)
salida=proc.stdout
ok('Menu integrado termina OK', proc.returncode==0, proc.returncode)
ok('Menu muestra BFS', 'Contactos por grado para el usuario: spez' in salida, '')
ok('Menu muestra Top 5', 'Top 5 terminos mas frecuentes' in salida, '')
ok('Menu muestra metricas hash', 'Metricas de la tabla hash' in salida, '')

for nombre, estado, detalle in resultados:
    print(('OK' if estado else 'FALLA') + ' - ' + nombre + (f' -> {detalle}' if detalle!='' else ''))

fallas=[r for r in resultados if not r[1]]
print('\nTOTAL:', len(resultados), 'pruebas')
print('FALLAS:', len(fallas))
if fallas:
    sys.exit(1)
