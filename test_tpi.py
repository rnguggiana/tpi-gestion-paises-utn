"""
Tests automáticos del TPI - Gestión de Países.

Cubre:
  1. Carga del CSV: parsing, conversión de tipos, manejo de errores.
  2. CRUD: agregar, actualizar, buscar (parcial y exacta).
  3. Filtros: continente, rango de población, rango de superficie.
  4. Ordenamientos: nombre, población, superficie (asc/desc).
  5. Estadísticas: mayor/menor, promedios, conteo por continente.
  6. Casos de borde: lista vacía, datos inválidos, rangos invertidos.
"""

import io
import os
import sys
import tempfile
import importlib.util
from pathlib import Path


HERE = Path(__file__).parent.resolve()
CODIGO_DIR = HERE / "codigo"
CSV_BASE = CODIGO_DIR / "paises.csv"

ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_YELLOW = "\033[93m"
ANSI_RESET = "\033[0m"

results: list[tuple[str, bool, str]] = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    icon = f"{ANSI_GREEN}PASS{ANSI_RESET}" if ok else f"{ANSI_RED}FAIL{ANSI_RESET}"
    line = f"  [{icon}] {name}"
    if detail and not ok:
        line += f"\n         -> {detail}"
    print(line)


def assert_eq(actual, expected, label):
    ok = actual == expected
    record(label, ok, f"esperaba {expected!r}, obtuvo {actual!r}")


def assert_in(needle, haystack, label):
    ok = needle in haystack
    record(label, ok, f"no se encontró {needle!r} en {haystack!r}")


# ---------------------------------------------------------------------------
# Setup: cargar los 3 módulos del proyecto
# ---------------------------------------------------------------------------
def cargar_modulos():
    """Carga los 3 módulos del proyecto en el namespace de testing."""
    sys.path.insert(0, str(CODIGO_DIR))

    spec_p = importlib.util.spec_from_file_location("paises", CODIGO_DIR / "paises.py")
    p_mod = importlib.util.module_from_spec(spec_p)
    sys.modules["paises"] = p_mod
    spec_p.loader.exec_module(p_mod)

    spec_f = importlib.util.spec_from_file_location("filtros", CODIGO_DIR / "filtros.py")
    f_mod = importlib.util.module_from_spec(spec_f)
    sys.modules["filtros"] = f_mod
    spec_f.loader.exec_module(f_mod)

    spec_e = importlib.util.spec_from_file_location("estadisticas", CODIGO_DIR / "estadisticas.py")
    e_mod = importlib.util.module_from_spec(spec_e)
    spec_e.loader.exec_module(e_mod)

    return p_mod, f_mod, e_mod


# ---------------------------------------------------------------------------
# Bloque 1: Carga del CSV
# ---------------------------------------------------------------------------
def test_carga_csv(p_mod):
    print(f"\n{ANSI_YELLOW}== Carga del CSV =={ANSI_RESET}")
    paises = p_mod.cargar_paises_desde_csv(str(CSV_BASE))

    record("CSV carga al menos 100 países", len(paises) >= 100,
           f"solo se cargaron {len(paises)}")
    record("Cada país es un diccionario", all(isinstance(p, dict) for p in paises))

    # Claves exactas
    primero = paises[0]
    for clave in ("nombre", "poblacion", "superficie", "continente"):
        record(f"Diccionario tiene clave '{clave}'", clave in primero)

    # Tipos correctos
    record("'poblacion' es int", isinstance(primero["poblacion"], int))
    record("'superficie' es int", isinstance(primero["superficie"], int))
    record("'nombre' es str", isinstance(primero["nombre"], str))
    record("'continente' es str", isinstance(primero["continente"], str))


def test_csv_no_existe(p_mod):
    print(f"\n{ANSI_YELLOW}== CSV no existe =={ANSI_RESET}")
    try:
        p_mod.cargar_paises_desde_csv("/ruta/inexistente/paises.csv")
        record("FileNotFoundError esperado", False, "no se lanzó")
    except FileNotFoundError:
        record("FileNotFoundError esperado", True)


def test_csv_malformado(p_mod):
    print(f"\n{ANSI_YELLOW}== CSV malformado =={ANSI_RESET}")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("col1,col2,col3\n")
        f.write("dato1,dato2,dato3\n")
        ruta = f.name
    try:
        try:
            p_mod.cargar_paises_desde_csv(ruta)
            record("CSV sin columnas correctas DEBE lanzar ValueError", False, "no se lanzó")
        except ValueError:
            record("CSV sin columnas correctas DEBE lanzar ValueError", True)
    finally:
        os.unlink(ruta)


# ---------------------------------------------------------------------------
# Bloque 2: Búsqueda
# ---------------------------------------------------------------------------
def test_busqueda(p_mod, paises):
    print(f"\n{ANSI_YELLOW}== Búsqueda =={ANSI_RESET}")

    # Exacta
    r = p_mod.buscar_por_nombre(paises, "Argentina", exacta=True)
    record("Búsqueda exacta 'Argentina' devuelve 1", len(r) == 1)
    record("Resultado es Argentina", r[0]["nombre"] == "Argentina")

    # Exacta case-insensitive
    r = p_mod.buscar_por_nombre(paises, "argentina", exacta=True)
    record("Búsqueda exacta case-insensitive", len(r) == 1 and r[0]["nombre"] == "Argentina")

    # Parcial
    r = p_mod.buscar_por_nombre(paises, "ar", exacta=False)
    record("Búsqueda parcial 'ar' devuelve >= 5", len(r) >= 5)

    # Sin resultados
    r = p_mod.buscar_por_nombre(paises, "PaisInexistente", exacta=False)
    record("Búsqueda sin resultados devuelve []", r == [])

    # encontrar_indice_por_nombre
    idx = p_mod.encontrar_indice_por_nombre(paises, "argentina")
    record("encontrar_indice_por_nombre (case-insens)", idx >= 0)
    idx = p_mod.encontrar_indice_por_nombre(paises, "PaisInexistente")
    record("encontrar_indice_por_nombre -> -1 si no existe", idx == -1)


# ---------------------------------------------------------------------------
# Bloque 3: Agregar
# ---------------------------------------------------------------------------
def test_agregar(p_mod):
    print(f"\n{ANSI_YELLOW}== Agregar país =={ANSI_RESET}")
    lista = []

    # Caso feliz
    p_mod.agregar_pais(lista, "Atlántida", 10000, 100, "Mítico")
    record("Caso feliz: agregó", len(lista) == 1)
    record("Datos correctos", lista[0]["nombre"] == "Atlántida" and lista[0]["poblacion"] == 10000)

    # Nombre vacío
    try:
        p_mod.agregar_pais(lista, "", 100, 100, "X")
        record("Nombre vacío DEBE lanzar ValueError", False)
    except ValueError:
        record("Nombre vacío DEBE lanzar ValueError", True)

    # Continente vacío
    try:
        p_mod.agregar_pais(lista, "Nuevo", 100, 100, "")
        record("Continente vacío DEBE lanzar ValueError", False)
    except ValueError:
        record("Continente vacío DEBE lanzar ValueError", True)

    # Población negativa
    try:
        p_mod.agregar_pais(lista, "Nuevo", -1, 100, "X")
        record("Población <= 0 DEBE lanzar ValueError", False)
    except ValueError:
        record("Población <= 0 DEBE lanzar ValueError", True)

    # Superficie 0
    try:
        p_mod.agregar_pais(lista, "Nuevo", 100, 0, "X")
        record("Superficie <= 0 DEBE lanzar ValueError", False)
    except ValueError:
        record("Superficie <= 0 DEBE lanzar ValueError", True)

    # Duplicado (case-insensitive)
    try:
        p_mod.agregar_pais(lista, "atlántida", 999, 999, "Y")
        record("Nombre duplicado DEBE lanzar ValueError", False)
    except ValueError:
        record("Nombre duplicado DEBE lanzar ValueError", True)


# ---------------------------------------------------------------------------
# Bloque 4: Actualizar
# ---------------------------------------------------------------------------
def test_actualizar(p_mod):
    print(f"\n{ANSI_YELLOW}== Actualizar país =={ANSI_RESET}")
    lista = [{"nombre": "X", "poblacion": 100, "superficie": 10, "continente": "Y"}]

    p_mod.actualizar_pais(lista, "X", nueva_poblacion=500)
    record("Actualiza solo población", lista[0]["poblacion"] == 500 and lista[0]["superficie"] == 10)

    p_mod.actualizar_pais(lista, "x", nueva_superficie=999)
    record("Actualiza solo superficie (case-insens)", lista[0]["superficie"] == 999)

    # No existe
    try:
        p_mod.actualizar_pais(lista, "NoExiste", nueva_poblacion=1)
        record("Actualizar país inexistente DEBE lanzar ValueError", False)
    except ValueError:
        record("Actualizar país inexistente DEBE lanzar ValueError", True)

    # Población negativa
    try:
        p_mod.actualizar_pais(lista, "X", nueva_poblacion=-1)
        record("Población <= 0 DEBE lanzar", False)
    except ValueError:
        record("Población <= 0 DEBE lanzar", True)


# ---------------------------------------------------------------------------
# Bloque 5: Filtros
# ---------------------------------------------------------------------------
def test_filtros(f_mod, paises):
    print(f"\n{ANSI_YELLOW}== Filtros =={ANSI_RESET}")

    # Continente
    amer = f_mod.filtrar_por_continente(paises, "América")
    record("Filtrar América: 22 países", len(amer) == 22)
    record("Todos del filtro son América", all(p["continente"] == "América" for p in amer))

    # Case-insensitive
    amer2 = f_mod.filtrar_por_continente(paises, "AMÉRICA")
    record("Filtrar continente case-insensitive", len(amer2) == len(amer))

    # Rango de población
    grandes = f_mod.filtrar_por_rango_poblacion(paises, 100_000_000, 2_000_000_000)
    record("Filtro >100M habitantes: >= 10", len(grandes) >= 10)
    record("Todos cumplen el rango", all(100_000_000 <= p["poblacion"] <= 2_000_000_000 for p in grandes))

    # Rango invertido DEBE lanzar
    try:
        f_mod.filtrar_por_rango_poblacion(paises, 1_000_000, 100)
        record("Rango invertido DEBE lanzar ValueError", False)
    except ValueError:
        record("Rango invertido DEBE lanzar ValueError", True)

    # Rango negativo DEBE lanzar
    try:
        f_mod.filtrar_por_rango_poblacion(paises, -10, 100)
        record("Rango negativo DEBE lanzar ValueError", False)
    except ValueError:
        record("Rango negativo DEBE lanzar ValueError", True)

    # Rango de superficie
    chicos = f_mod.filtrar_por_rango_superficie(paises, 0, 100_000)
    record("Filtro superficie < 100K km²: >= 5", len(chicos) >= 5)
    record("Todos cumplen el rango de superficie",
           all(0 <= p["superficie"] <= 100_000 for p in chicos))


# ---------------------------------------------------------------------------
# Bloque 6: Ordenamientos
# ---------------------------------------------------------------------------
def test_ordenamientos(f_mod, paises):
    print(f"\n{ANSI_YELLOW}== Ordenamientos =={ANSI_RESET}")

    # Por nombre asc
    por_nom = f_mod.ordenar_por_nombre(paises)
    nombres = [p["nombre"] for p in por_nom]
    record("Orden por nombre asc: primero alfabético", nombres[0].lower() <= nombres[-1].lower())

    # Por nombre desc
    por_nom_desc = f_mod.ordenar_por_nombre(paises, descendente=True)
    record("Orden por nombre desc invierte el primero",
           por_nom_desc[0]["nombre"] != por_nom[0]["nombre"])

    # Por población desc
    por_pob = f_mod.ordenar_por_poblacion(paises, descendente=True)
    record("Mayor población es China", por_pob[0]["nombre"] == "China")
    record("Top 2 incluye India", por_pob[1]["nombre"] == "India")

    # Por superficie desc
    por_sup = f_mod.ordenar_por_superficie(paises, descendente=True)
    record("Mayor superficie es Rusia", por_sup[0]["nombre"] == "Rusia")

    # No muta la lista original
    original_len = len(paises)
    f_mod.ordenar_por_nombre(paises)
    record("Ordenar NO muta lista original", len(paises) == original_len)


# ---------------------------------------------------------------------------
# Bloque 7: Estadísticas
# ---------------------------------------------------------------------------
def test_estadisticas(e_mod, paises):
    print(f"\n{ANSI_YELLOW}== Estadísticas =={ANSI_RESET}")

    mayor = e_mod.pais_mayor_poblacion(paises)
    record("Mayor población: China", mayor["nombre"] == "China")

    menor = e_mod.pais_menor_poblacion(paises)
    record("Menor población es válido", isinstance(menor, dict) and menor["poblacion"] > 0)

    prom_pob = e_mod.promedio_poblacion(paises)
    record("Promedio población > 0", prom_pob > 0)

    prom_sup = e_mod.promedio_superficie(paises)
    record("Promedio superficie > 0", prom_sup > 0)

    por_cont = e_mod.cantidad_por_continente(paises)
    record("Continentes: 5 distintos", len(por_cont) == 5)
    record("Asia es el más numeroso", list(por_cont.keys())[0] == "Asia")
    record("Total continentes coincide con dataset",
           sum(por_cont.values()) == len(paises))


def test_estadisticas_vacio(e_mod):
    print(f"\n{ANSI_YELLOW}== Estadísticas con lista vacía =={ANSI_RESET}")
    record("Mayor de [] es None", e_mod.pais_mayor_poblacion([]) is None)
    record("Menor de [] es None", e_mod.pais_menor_poblacion([]) is None)
    record("Promedio de [] es 0", e_mod.promedio_poblacion([]) == 0)
    record("Promedio sup [] es 0", e_mod.promedio_superficie([]) == 0)
    record("Conteo [] es dict vacío", e_mod.cantidad_por_continente([]) == {})


# ---------------------------------------------------------------------------
# Bloque 8: Validaciones de helpers
# ---------------------------------------------------------------------------
def test_helpers(p_mod):
    print(f"\n{ANSI_YELLOW}== Helpers de validación =={ANSI_RESET}")

    # normalizar
    assert_eq(p_mod.normalizar("Argentina"), "argentina", "normalizar 'Argentina'")
    assert_eq(p_mod.normalizar("  ARGENTINA  "), "argentina", "normalizar con espacios")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"{ANSI_YELLOW}{'=' * 70}{ANSI_RESET}")
    print(f"{ANSI_YELLOW}Tests automáticos del TPI - Gestión de Países{ANSI_RESET}")
    print(f"{ANSI_YELLOW}{'=' * 70}{ANSI_RESET}")

    p_mod, f_mod, e_mod = cargar_modulos()

    # Cargar dataset una vez para los tests que lo necesitan
    paises = p_mod.cargar_paises_desde_csv(str(CSV_BASE))

    test_carga_csv(p_mod)
    test_csv_no_existe(p_mod)
    test_csv_malformado(p_mod)
    test_busqueda(p_mod, paises)
    test_agregar(p_mod)
    test_actualizar(p_mod)
    test_filtros(f_mod, paises)
    test_ordenamientos(f_mod, paises)
    test_estadisticas(e_mod, paises)
    test_estadisticas_vacio(e_mod)
    test_helpers(p_mod)

    print(f"\n{ANSI_YELLOW}{'=' * 70}{ANSI_RESET}")
    print(f"{ANSI_YELLOW}RESUMEN{ANSI_RESET}")
    print(f"{ANSI_YELLOW}{'=' * 70}{ANSI_RESET}")
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed
    print(f"  Total : {total}")
    print(f"  {ANSI_GREEN}Pasaron: {passed}{ANSI_RESET}")
    if failed:
        print(f"  {ANSI_RED}Fallaron: {failed}{ANSI_RESET}")
        for name, ok, detail in results:
            if not ok:
                print(f"    - {name}")
                if detail:
                    print(f"        {detail}")
        return 1
    print(f"  {ANSI_GREEN}Todos los tests pasaron.{ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
