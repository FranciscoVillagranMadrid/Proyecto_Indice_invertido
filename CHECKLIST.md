# Checklist de pruebas — Proyecto 2

Usa esta lista para verificar que todo funciona antes de entregar.

---

## Entrega 1 — lo que ya funcionaba

- [ ] El programa arranca sin errores (`python red_social.py`)
- [ ] El resumen inicial muestra usuarios, posts, relaciones, stopwords y términos indexados
- [ ] Opción 1: buscar un término que existe (por ejemplo `python`) devuelve posts
- [ ] Opción 1: buscar una stopword (por ejemplo `the`) dice que no hay resultados
- [ ] Opción 1: buscar un término que no existe dice que no hay resultados sin caerse
- [ ] Opción 1: escribir `TERMINOS` muestra algunos términos del índice
- [ ] Opción 2: buscar un usuario que existe (por ejemplo `spez`) muestra sus contactos
- [ ] Opción 2: buscar un usuario que no existe avisa sin caerse
- [ ] Opción 2: escribir `USUARIOS` muestra algunos usuarios del índice
- [ ] Opción 3: muestra algunos posts cargados en memoria
- [ ] Opción 4: muestra el resumen de carga

---

## Entrega 2 — grafo y BFS

- [ ] El resumen inicial muestra "Usuarios en el grafo: X" con un número mayor a 0
- [ ] Opción 5: ingresar un usuario válido muestra grados 1°, 2° y 3°
- [ ] Opción 5: el usuario raíz NO aparece como contacto en ningún grado
- [ ] Opción 5: no hay usuarios repetidos entre distintos grados
- [ ] Opción 5: un usuario de 1° no aparece también en 2° ni en 3°
- [ ] Opción 5: un usuario sin contactos muestra "(sin contactos en este grado)" en todos los grados
- [ ] Opción 5: un usuario que no existe avisa sin caerse

---

## Entrega 3 — tabla hash

- [ ] El resumen inicial muestra "Terminos en tabla hash: X" igual al valor de "Terminos indexados"
- [ ] Opción 6: ingresar `5` muestra el Top-5 ordenado de mayor a menor frecuencia
- [ ] Opción 6: ingresar `10` muestra el Top-10 ordenado
- [ ] Opción 6: ingresar `20` muestra el Top-20 ordenado
- [ ] Opción 6: ingresar un valor distinto a 5/10/20 dice que es inválido sin caerse
- [ ] Opción 7: muestra N, M, factor de carga, colisiones, largo máximo y promedio de cadenas
- [ ] Opción 7: M es mayor o igual a 1.5 × N
- [ ] Opción 7: el factor de carga = N / M (verificar con calculadora)

---

## Robustez general del menú

- [ ] Ingresar una letra o número inválido (por ejemplo `9`, `abc`) dice "Opción no válida"
- [ ] El programa no se cae ante ninguna entrada inválida
- [ ] La opción 8 cierra el programa correctamente

---

## Archivos del proyecto (verificar que todos estén presentes)

```
listas.py              ← sin cambios (Entrega 1)
indices.py             ← sin cambios (Entrega 1)
red_social.py          ← modificado (agrega opciones 5, 6, 7, 8)
preprocesar_reddit.py  ← sin cambios (auxiliar)
grafo_contactos.py     ← nuevo (Entrega 2)
tabla_hash.py          ← nuevo (Entrega 3)
usuarios.csv
posts.csv
relaciones.csv
stopwords.txt
README.md
```
