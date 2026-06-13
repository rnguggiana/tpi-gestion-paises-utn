# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**
**Tecnicatura Universitaria en Programación a Distancia — UTN**

## Integrantes

- **Matias Fernando Nuñez**
- **Rodrigo Nahuel Guggiana**

## Descripción

Aplicación de consola en Python que gestiona un dataset de **120 países** cargado desde un archivo CSV. El código permite agregar, actualizar, buscar, filtrar, ordenar y generar estadísticas sobre el catálogo de paises.

El sistema implementa los conceptos centrales que aprendidos en la materia: **listas**, **diccionarios**, **funciones**, **estructuras condicionales y repetitivas**, **lectura/escritura de CSV**, **manejo de errores con `try/except`** y **modularización**.

## Enlaces

- 📂 **Repositorio GitHub**: <https://github.com/matiasfnunezdev/tpi-gestion-paises-utn>
- 📹 **Video demostrativo**: [`COMPLETAR_LINK_YOUTUBE`](#) (pendiente de grabación)
- 📄 **Documentación PDF**: [`docs/documentacion.pdf`](docs/documentacion.pdf)

## Estructura del proyecto

```
trabajo-practico-integrador/
├── codigo/
│   ├── main.py             # Punto de entrada con el menú
│   ├── paises.py           # CRUD + búsqueda + helpers de validación
│   ├── filtros.py          # Filtros y ordenamientos
│   ├── estadisticas.py     # Cálculos estadísticos
│   └── paises.csv          # Dataset base (120 países)
├── docs/
│   ├── documentacion.md    # Fuente Markdown del informe
│   ├── documentacion.docx  # Word generado
│   └── documentacion.pdf   # Documento académico de entrega
├── entrega/
│   └── TPI_Programacion_1.zip   # Paquete final
├── enunciado-tpi.md
├── test_tpi.py             # 59 tests automáticos
└── README.md               # Este archivo
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

### Cómo ejecutar los tests

```bash
PYTHONIOENCODING=utf-8 python test_tpi.py
```

Cubre **59 casos**: carga del CSV, CRUD, búsquedas (parcial/exacta), filtros (con rangos válidos e inválidos), ordenamientos, estadísticas (incluyendo lista vacía) y validaciones de helpers.

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
| **Funciones** | Modularización: 1 función por responsabilidad en 4 archivos |
| **Condicionales** | Menú, validaciones, manejo de casos de borde |
| **Bucles** | Recorrido de la lista, menú persistente |
| **Ordenamientos** | `sorted()` con `key=` y `reverse=` |
| **Estadísticas básicas** | `max`, `min`, promedios, conteos |
| **Archivos CSV** | Módulo `csv` con `DictReader` y `DictWriter` |
| **Manejo de errores** | `try/except` + `raise ValueError` con mensajes claros |

## Participación de los integrantes

- **Matias Fernando Nuñez**: arquitectura general, módulos `paises.py` y `main.py`, tests automáticos.
- **Rodrigo Nahuel Guggiana**: módulos `filtros.py`, `estadisticas.py`, dataset CSV, documentación técnica.

## Bibliografía y referencias

- **Documentación oficial de Python**: <https://docs.python.org/es/3/>
- **Módulo csv**: <https://docs.python.org/es/3/library/csv.html>
- **Módulo os**: <https://docs.python.org/es/3/library/os.html>
- **Manejo de excepciones**: <https://docs.python.org/es/3/tutorial/errors.html>
- **PEP 8 — Style Guide**: <https://peps.python.org/pep-0008/>
- **Material de la cátedra UTN — Programación 1, 2026**.


