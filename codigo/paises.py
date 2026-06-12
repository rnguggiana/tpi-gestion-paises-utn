"""
Módulo: paises.py
Responsabilidad: CRUD de países + búsquedas.

Trabaja sobre una lista de diccionarios donde cada país tiene las claves:
    'nombre', 'poblacion', 'superficie', 'continente'

Las funciones reciben la lista como parámetro (sin variables globales) y
modifican esa misma lista cuando corresponde (las listas son mutables en
Python, así que los cambios se propagan).
"""

import csv
import os


CLAVES_REQUERIDAS = ("nombre", "poblacion", "superficie", "continente")


# ---------------------------------------------------------------------------
# Helpers de validación reutilizables (encapsulan try/except + casos de borde)
# ---------------------------------------------------------------------------
def pedir_entero(mensaje, min_valor=None):
    """Pide un entero al usuario.

    Lanza ValueError con mensaje descriptivo si:
        - la entrada está vacía o solo tiene espacios,
        - no se puede convertir a int,
        - es menor que min_valor (si se indica).
    """
    texto = input(mensaje).strip()
    if not texto:
        raise ValueError("La entrada no puede estar vacía o contener solo espacios.")
    valor = int(texto)
    if min_valor is not None and valor < min_valor:
        raise ValueError(f"El valor debe ser mayor o igual a {min_valor}.")
    return valor


def pedir_entero_con_reintentos(mensaje, min_valor=None):
    """Versión que insiste hasta obtener un valor válido."""
    while True:
        try:
            return pedir_entero(mensaje, min_valor)
        except ValueError as e:
            print(f"  Error: {e}. Intente nuevamente.")


def pedir_texto_no_vacio(mensaje):
    """Pide un texto y rechaza vacío o solo espacios."""
    texto = input(mensaje)
    if not texto.strip():
        raise ValueError("El texto no puede estar vacío ni contener solo espacios.")
    return texto


def normalizar(texto):
    """Normaliza un texto para comparaciones (strip + lower)."""
    return texto.strip().lower()


# ---------------------------------------------------------------------------
# Lectura del CSV
# ---------------------------------------------------------------------------
def cargar_paises_desde_csv(ruta_csv):
    """Lee paises.csv y devuelve una lista de diccionarios.

    Aplica conversiones de tipo: poblacion e int. Si una fila está
    malformada, la salta e imprime una advertencia (no rompe todo el
    programa). Si el archivo no existe, lanza FileNotFoundError.
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo CSV en '{ruta_csv}'.")

    paises = []
    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        # Validar que el CSV tenga las columnas esperadas
        if lector.fieldnames is None or not all(c in lector.fieldnames for c in CLAVES_REQUERIDAS):
            raise ValueError(
                f"El CSV debe tener las columnas {CLAVES_REQUERIDAS}. "
                f"Encontradas: {lector.fieldnames}"
            )

        for nro_fila, fila in enumerate(lector, start=2):  # start=2: la línea 1 es header
            try:
                pais = {
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip(),
                }
                # Validación de campos vacíos
                if not pais["nombre"] or not pais["continente"]:
                    raise ValueError("nombre o continente vacíos")
                paises.append(pais)
            except (ValueError, KeyError) as e:
                print(f"  Advertencia: fila {nro_fila} del CSV ignorada ({e}).")
    return paises


def guardar_paises_en_csv(paises, ruta_csv):
    """Persiste la lista de países al CSV (sobreescribe el archivo)."""
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CLAVES_REQUERIDAS)
        escritor.writeheader()
        escritor.writerows(paises)


# ---------------------------------------------------------------------------
# Búsqueda
# ---------------------------------------------------------------------------
def buscar_por_nombre(paises, texto_busqueda, exacta=False):
    """Devuelve la lista de países cuyo nombre coincida.

    Si exacta=True compara strings normalizados al 100%. Si False, devuelve
    todos los que contengan el texto buscado (búsqueda parcial).
    """
    consulta = normalizar(texto_busqueda)
    if exacta:
        return [p for p in paises if normalizar(p["nombre"]) == consulta]
    return [p for p in paises if consulta in normalizar(p["nombre"])]


def encontrar_indice_por_nombre(paises, nombre):
    """Devuelve el índice exacto (case-insensitive) o -1 si no existe."""
    consulta = normalizar(nombre)
    for i, p in enumerate(paises):
        if normalizar(p["nombre"]) == consulta:
            return i
    return -1


# ---------------------------------------------------------------------------
# Alta / actualización
# ---------------------------------------------------------------------------
def agregar_pais(paises, nombre, poblacion, superficie, continente):
    """Agrega un país nuevo a la lista. Lanza ValueError si datos inválidos.

    Reglas:
        - Ningún campo puede estar vacío.
        - poblacion y superficie deben ser enteros > 0.
        - El nombre no puede estar duplicado (case-insensitive).
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")
    if not continente or not continente.strip():
        raise ValueError("El continente no puede estar vacío.")
    if not isinstance(poblacion, int) or poblacion <= 0:
        raise ValueError("La población debe ser un entero positivo.")
    if not isinstance(superficie, int) or superficie <= 0:
        raise ValueError("La superficie debe ser un entero positivo.")
    if encontrar_indice_por_nombre(paises, nombre) != -1:
        raise ValueError(f"El país '{nombre.strip()}' ya existe.")

    paises.append({
        "nombre": nombre.strip(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.strip(),
    })


def actualizar_pais(paises, nombre, nueva_poblacion=None, nueva_superficie=None):
    """Actualiza población y/o superficie de un país existente.

    Lanza ValueError si el país no existe o si los valores son inválidos.
    Devuelve el diccionario del país actualizado.
    """
    indice = encontrar_indice_por_nombre(paises, nombre)
    if indice == -1:
        raise ValueError(f"El país '{nombre.strip()}' no se encuentra en el catálogo.")

    if nueva_poblacion is not None:
        if not isinstance(nueva_poblacion, int) or nueva_poblacion <= 0:
            raise ValueError("La nueva población debe ser un entero positivo.")
        paises[indice]["poblacion"] = nueva_poblacion

    if nueva_superficie is not None:
        if not isinstance(nueva_superficie, int) or nueva_superficie <= 0:
            raise ValueError("La nueva superficie debe ser un entero positivo.")
        paises[indice]["superficie"] = nueva_superficie

    return paises[indice]


# ---------------------------------------------------------------------------
# Listado / display
# ---------------------------------------------------------------------------
def mostrar_paises(paises, titulo="Países"):
    """Imprime una tabla legible con los países."""
    if not paises:
        print(f"\n  {titulo}: (sin resultados)")
        return

    print(f"\n=== {titulo} ({len(paises)} resultado/s) ===")
    print(f"{'#':<4} {'Nombre':<30} {'Población':>15} {'Superficie km²':>15} {'Continente':<12}")
    print("-" * 80)
    for i, p in enumerate(paises, start=1):
        print(
            f"{i:<4} {p['nombre']:<30} {p['poblacion']:>15,} {p['superficie']:>15,} {p['continente']:<12}"
        )
    print("-" * 80)
