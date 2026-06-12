"""
================================================================
Trabajo Práctico Integrador (TPI) - Programación 1 - UTN
Gestión de Datos de Países en Python

Integrantes:
    - Matias Fernando Nuñez
    - Rodrigo Nahuel Guggiana

Fecha: 6 de junio de 2026
================================================================

main.py - Punto de entrada del sistema.
Responsabilidad: presentar el menú interactivo y delegar a los módulos
de dominio (paises, filtros, estadisticas).

El programa carga el dataset desde 'paises.csv' al iniciar y mantiene
la lista de países en memoria como una lista de diccionarios. Al
modificar el dataset (agregar / actualizar), se persiste de nuevo en
el CSV para que los cambios sobrevivan al cierre del programa.
"""

import os
import sys

# Importar módulos del proyecto
import paises as p_mod
import filtros as f_mod
import estadisticas as e_mod


# Ruta del CSV: relativa a la ubicación de main.py
RUTA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paises.csv")


# ===========================================================================
# === Opciones del menú
# ===========================================================================

def opcion_1_mostrar_todos(paises):
    """Muestra el dataset completo."""
    p_mod.mostrar_paises(paises, titulo="Dataset completo de países")


def opcion_2_agregar_pais(paises):
    """Agrega un país nuevo al dataset y persiste en el CSV."""
    print("\n=== Agregar nuevo país ===")
    try:
        nombre = p_mod.pedir_texto_no_vacio("  Nombre: ")
        continente = p_mod.pedir_texto_no_vacio("  Continente: ")
        poblacion = p_mod.pedir_entero("  Población (entero > 0): ", min_valor=1)
        superficie = p_mod.pedir_entero("  Superficie en km² (entero > 0): ", min_valor=1)

        p_mod.agregar_pais(paises, nombre, poblacion, superficie, continente)
        p_mod.guardar_paises_en_csv(paises, RUTA_CSV)
        print(f"  País '{nombre.strip()}' agregado exitosamente y guardado en CSV.")
    except ValueError as e:
        print(f"  Error: {e}. No se agregó el país.")


def opcion_3_actualizar_pais(paises):
    """Actualiza población y/o superficie de un país existente."""
    print("\n=== Actualizar país ===")
    try:
        nombre = p_mod.pedir_texto_no_vacio("  Nombre del país a actualizar: ")
    except ValueError as e:
        print(f"  Error: {e}")
        return

    indice = p_mod.encontrar_indice_por_nombre(paises, nombre)
    if indice == -1:
        print(f"  El país '{nombre.strip()}' no se encuentra en el catálogo.")
        return

    actual = paises[indice]
    print(f"  Datos actuales: población = {actual['poblacion']:,}, superficie = {actual['superficie']:,} km²")
    print("  Deje en blanco un campo si NO desea modificarlo.")

    nueva_pob = None
    nueva_sup = None
    try:
        entrada_pob = input("  Nueva población (Enter para no cambiar): ").strip()
        if entrada_pob:
            nueva_pob = int(entrada_pob)
            if nueva_pob <= 0:
                raise ValueError("La nueva población debe ser entero positivo.")

        entrada_sup = input("  Nueva superficie (Enter para no cambiar): ").strip()
        if entrada_sup:
            nueva_sup = int(entrada_sup)
            if nueva_sup <= 0:
                raise ValueError("La nueva superficie debe ser entero positivo.")

        if nueva_pob is None and nueva_sup is None:
            print("  No se modificó ningún campo.")
            return

        p_mod.actualizar_pais(paises, nombre, nueva_pob, nueva_sup)
        p_mod.guardar_paises_en_csv(paises, RUTA_CSV)
        print(f"  País '{actual['nombre']}' actualizado y guardado en CSV.")
    except ValueError as e:
        print(f"  Error: {e}")


def opcion_4_buscar_por_nombre(paises):
    """Busca por nombre con coincidencia parcial o exacta."""
    print("\n=== Buscar país por nombre ===")
    try:
        texto = p_mod.pedir_texto_no_vacio("  Texto a buscar: ")
        print("  Tipo de búsqueda: 1) Exacta  2) Parcial (contiene el texto)")
        tipo = p_mod.pedir_entero("  Seleccione (1 o 2): ", min_valor=1)
        if tipo not in (1, 2):
            raise ValueError("La opción debe ser 1 o 2.")

        resultados = p_mod.buscar_por_nombre(paises, texto, exacta=(tipo == 1))
        if not resultados:
            print(f"  No se encontró ningún país que coincida con '{texto.strip()}'.")
        else:
            p_mod.mostrar_paises(resultados, titulo=f"Resultados para '{texto.strip()}'")
    except ValueError as e:
        print(f"  Error: {e}")


def opcion_5_filtrar(paises):
    """Submenú de filtros: continente, rango población, rango superficie."""
    print("\n=== Filtrar países ===")
    print("  1. Por continente")
    print("  2. Por rango de población")
    print("  3. Por rango de superficie")
    print("  0. Volver")

    try:
        opcion = p_mod.pedir_entero("  Seleccione: ", min_valor=0)
    except ValueError as e:
        print(f"  Error: {e}")
        return

    if opcion == 0:
        return

    try:
        if opcion == 1:
            continente = p_mod.pedir_texto_no_vacio("  Continente (América/Europa/Asia/África/Oceanía): ")
            resultado = f_mod.filtrar_por_continente(paises, continente)
            p_mod.mostrar_paises(resultado, titulo=f"Países en {continente.strip()}")
        elif opcion == 2:
            minimo = p_mod.pedir_entero("  Población mínima: ", min_valor=0)
            maximo = p_mod.pedir_entero("  Población máxima: ", min_valor=0)
            resultado = f_mod.filtrar_por_rango_poblacion(paises, minimo, maximo)
            p_mod.mostrar_paises(resultado, titulo=f"Países con población entre {minimo:,} y {maximo:,}")
        elif opcion == 3:
            minimo = p_mod.pedir_entero("  Superficie mínima (km²): ", min_valor=0)
            maximo = p_mod.pedir_entero("  Superficie máxima (km²): ", min_valor=0)
            resultado = f_mod.filtrar_por_rango_superficie(paises, minimo, maximo)
            p_mod.mostrar_paises(resultado, titulo=f"Países con superficie entre {minimo:,} y {maximo:,} km²")
        else:
            print("  Opción de filtro inválida.")
    except ValueError as e:
        print(f"  Error: {e}")


def opcion_6_ordenar(paises):
    """Submenú de ordenamientos."""
    print("\n=== Ordenar países ===")
    print("  1. Por nombre")
    print("  2. Por población")
    print("  3. Por superficie")
    print("  0. Volver")

    try:
        criterio = p_mod.pedir_entero("  Criterio: ", min_valor=0)
        if criterio == 0:
            return
        if criterio not in (1, 2, 3):
            raise ValueError("Criterio inválido. Seleccione 1, 2 o 3.")

        print("  Sentido: 1) Ascendente  2) Descendente")
        sentido = p_mod.pedir_entero("  Seleccione: ", min_valor=1)
        if sentido not in (1, 2):
            raise ValueError("El sentido debe ser 1 (asc) o 2 (desc).")

        descendente = (sentido == 2)
        if criterio == 1:
            ordenado = f_mod.ordenar_por_nombre(paises, descendente=descendente)
            titulo = f"Ordenado por nombre ({'desc' if descendente else 'asc'})"
        elif criterio == 2:
            ordenado = f_mod.ordenar_por_poblacion(paises, descendente=descendente)
            titulo = f"Ordenado por población ({'desc' if descendente else 'asc'})"
        else:
            ordenado = f_mod.ordenar_por_superficie(paises, descendente=descendente)
            titulo = f"Ordenado por superficie ({'desc' if descendente else 'asc'})"

        p_mod.mostrar_paises(ordenado, titulo=titulo)
    except ValueError as e:
        print(f"  Error: {e}")


def opcion_7_estadisticas(paises):
    """Muestra todas las estadísticas del dataset."""
    e_mod.mostrar_estadisticas(paises)


def opcion_8_salir():
    """Mensaje de despedida."""
    print("\nGracias por usar el sistema de gestión de países. Hasta luego.")


# ===========================================================================
# === Menú principal
# ===========================================================================

def mostrar_menu():
    """Imprime el menú con las 8 opciones."""
    print("\n" + "=" * 60)
    print("GESTIÓN DE PAÍSES - Trabajo Práctico Integrador")
    print("=" * 60)
    print("  1. Mostrar todos los países")
    print("  2. Agregar país")
    print("  3. Actualizar país (población / superficie)")
    print("  4. Buscar país por nombre")
    print("  5. Filtrar países (continente / rango)")
    print("  6. Ordenar países")
    print("  7. Mostrar estadísticas")
    print("  8. Salir")
    print("=" * 60)


def menu_principal():
    """Carga el CSV al inicio y entra en el bucle del menú."""
    try:
        paises = p_mod.cargar_paises_desde_csv(RUTA_CSV)
        print(f"\n[OK] Se cargaron {len(paises)} países desde 'paises.csv'.")
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("Cree un archivo 'paises.csv' en la misma carpeta que main.py.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] El CSV tiene un formato inválido: {e}")
        sys.exit(1)

    while True:
        mostrar_menu()
        try:
            opcion = p_mod.pedir_entero("Seleccione una opción (1-8): ", min_valor=1)
        except ValueError as e:
            print(f"  Error: {e}. Intente nuevamente.")
            continue

        if opcion == 1:
            opcion_1_mostrar_todos(paises)
        elif opcion == 2:
            opcion_2_agregar_pais(paises)
        elif opcion == 3:
            opcion_3_actualizar_pais(paises)
        elif opcion == 4:
            opcion_4_buscar_por_nombre(paises)
        elif opcion == 5:
            opcion_5_filtrar(paises)
        elif opcion == 6:
            opcion_6_ordenar(paises)
        elif opcion == 7:
            opcion_7_estadisticas(paises)
        elif opcion == 8:
            opcion_8_salir()
            break
        else:
            print("  Opción fuera de rango. Seleccione del 1 al 8.")


if __name__ == "__main__":
    menu_principal()
