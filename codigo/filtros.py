# Funciones para filtrar y ordenar países.

from paises import normalizar

# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------
def filtrar_por_continente(paises, continente):                                                            # Devuelve los países cuyo continente coincida (case-insensitive).
    consulta = normalizar(continente)
    return [p for p in paises if normalizar(p["continente"]) == consulta]


def filtrar_por_rango_poblacion(paises, minimo, maximo):                                                   # Devuelve los países con población entre minimo y maximo inclusive. Lanza ValueError si minimo > maximo o si alguno es negativo.
    if minimo < 0 or maximo < 0:
        raise ValueError("Los valores del rango no pueden ser negativos.")
    if minimo > maximo:
        raise ValueError(f"El mínimo ({minimo:,}) no puede ser mayor que el máximo ({maximo:,}).")
    return [p for p in paises if minimo <= p["poblacion"] <= maximo]


def filtrar_por_rango_superficie(paises, minimo, maximo):                                                  # Devuelve los países con superficie entre minimo y maximo inclusive.
    if minimo < 0 or maximo < 0:
        raise ValueError("Los valores del rango no pueden ser negativos.")
    if minimo > maximo:
        raise ValueError(f"El mínimo ({minimo:,}) no puede ser mayor que el máximo ({maximo:,}).")
    return [p for p in paises if minimo <= p["superficie"] <= maximo]


# ---------------------------------------------------------------------------
# Ordenamientos
# ---------------------------------------------------------------------------
def ordenar_por_nombre(paises, descendente=False):                                                         # Ordena alfabéticamente por nombre.
    return sorted(paises, key=lambda p: normalizar(p["nombre"]), reverse=descendente)


def ordenar_por_poblacion(paises, descendente=False):                                                      # Ordena por población.  
        return sorted(paises, key=lambda p: p["poblacion"], reverse=descendente)


def ordenar_por_superficie(paises, descendente=False):                                                     # Ordena por superficie.
    return sorted(paises, key=lambda p: p["superficie"], reverse=descendente)
