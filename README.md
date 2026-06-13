# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**
**Tecnicatura Universitaria en Programación a Distancia — UTN**

## Integrantes

- **Matias Fernando Nuñez**
- **Rodrigo Nahuel Guggiana**

## Descripción

Aplicación de consola en Python para trabajar con un archivo CSV de países. El programa permite mostrar los datos cargados, agregar y actualizar países, buscar por nombre, filtrar, ordenar y ver algunas estadísticas básicas.

Para resolverlo usamos contenidos vistos en Programación I, como listas, diccionarios, funciones, condicionales, bucles, archivos CSV y manejo de errores con try/except. También separamos el código en varios archivos para que fuera más fácil de leer y probar.

## Enlaces

- **Repositorio GitHub**: <https://github.com/matiasfnunezdev/tpi-gestion-paises-utn>
- **Video demostrativo**: [`COMPLETAR_LINK_YOUTUBE`](#) (pendiente de grabación)
- **Documentación PDF**: [`docs/documentacion.pdf`](docs/documentacion.pdf)

## Estructura del proyecto

```
tpi-gestion-paises-utn/
├── codigo/
│   ├── main.py
│   ├── paises.py
│   ├── filtros.py
│   ├── estadisticas.py
│   └── paises.csv
├── docs/
│   └── documentacion.pdf
├── README.md
└── test_tpi.py
```

## Instalación y ejecución

### Requisitos

- Python 3.8 o superior.
- Sin dependencias externas (solo módulos de la biblioteca estándar: `csv`, `os`, `sys`).

### Cómo ejecutar

```bash
cd codigo
python main.py
```

El programa carga automáticamente `paises.csv` y muestra el menú principal. Si el CSV está malformado o no se encuentra, lo informa con un mensaje claro y termina.

### Archivo de pruebas

También dejamos un archivo `test_tpi.py` que usamos para revisar varias funciones del programa sin tener que probar todo manualmente desde el menú.

## Ejemplo de entradas/salidas

### Inicio del programa

```
[OK] Se cargaron 120 países desde 'paises.csv'.

============================================================
GESTIÓN DE PAÍSES - Trabajo Práctico Integrador
============================================================
  1. Mostrar todos los países
  2. Agregar país
  3. Actualizar país (población / superficie)
  4. Buscar país por nombre
  5. Filtrar países (continente / rango)
  6. Ordenar países
  7. Mostrar estadísticas
  8. Salir
============================================================
Seleccione una opción (1-8):
```

### Búsqueda parcial

```
Seleccione una opción (1-8): 4

=== Buscar país por nombre ===
  Texto a buscar: ar
  Tipo de búsqueda: 1) Exacta  2) Parcial (contiene el texto)
  Seleccione (1 o 2): 2

=== Resultados para 'ar' (11 resultado/s) ===
#    Nombre                              Población   Superficie km²  Continente
--------------------------------------------------------------------------------
1    Argentina                         45,376,763           2,780,400 América
2    Arabia Saudita                    34,813,871           2,149,690 Asia
3    Argelia                           43,851,044           2,381,741 África
...
```

### Estadísticas

```
=== Estadísticas del dataset ===
  Total de países cargados: 120

  País con MAYOR población: China (1,439,323,776 habitantes)
  País con MENOR población: Samoa (198,414 habitantes)

  Promedio de población :       62,087,051.13 habitantes
  Promedio de superficie:        1,019,237.43 km²

  Cantidad de países por continente:
    Asia        : 36 países
    Europa      : 34 países
    América     : 22 países
    África      : 22 países
    Oceanía     : 6 países
```

### Filtro por rango de población

```
=== Filtrar países ===
  1. Por continente
  2. Por rango de población
  3. Por rango de superficie
  0. Volver
  Seleccione: 2
  Población mínima: 100000000
  Población máxima: 2000000000

=== Países con población entre 100,000,000 y 2,000,000,000 (14 resultado/s) ===
...
```

### Caso de error: agregar país duplicado

```
=== Agregar nuevo país ===
  Nombre: Argentina
  Continente: América
  Población (entero > 0): 50000000
  Superficie en km² (entero > 0): 2780400
  Error: El país 'Argentina' ya existe. No se agregó el país.
```

## Conceptos aplicados

| Concepto | Dónde |
|---|---|
| **Listas** | `paises[]` como estructura principal |
| **Diccionarios** | Cada país es un `dict` con 4 claves |
| **Funciones** | Separación del programa en funciones para ordenar mejor el código |
| **Condicionales** | Menú, validaciones, manejo de casos de borde |
| **Bucles** | Recorrido de la lista, menú persistente |
| **Ordenamientos** | `sorted()` con `key=` y `reverse=` |
| **Estadísticas básicas** | `max`, `min`, promedios, conteos |
| **Archivos CSV** | Módulo `csv` con `DictReader` y `DictWriter` |
| **Manejo de errores** | Uso de `try/except` para entradas inválidas y errores del archivo |

## Participación de los integrantes

- **Matias Fernando Nuñez**: trabajó principalmente en la estructura inicial del proyecto, el menú principal, el módulo `paises.py`, la carga y guardado del CSV, validaciones principales y archivo de pruebas.

- **Rodrigo Nahuel Guggiana**: trabajó principalmente en el dataset de países, los filtros por continente, población y superficie, los ordenamientos, el módulo de estadísticas y la revisión de funcionamiento de esas opciones.

Ambos integrantes revisamos el programa completo, probamos el menú y participamos en la preparación de la entrega final.

## Bibliografía y referencias

- **Documentación oficial de Python**: <https://docs.python.org/es/3/>
- **Módulo csv**: <https://docs.python.org/es/3/library/csv.html>
- **Módulo os**: <https://docs.python.org/es/3/library/os.html>
- **Manejo de excepciones**: <https://docs.python.org/es/3/tutorial/errors.html>
- **Material de la cátedra UTN — Programación 1, 2026**.


