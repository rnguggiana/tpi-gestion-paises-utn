# Funciones para estadisticas

def pais_mayor_poblacion(paises):                                                # Devuelve el país con MAYOR población. None si la lista está vacía
    if not paises:
        return None
    return max(paises, key=lambda p: p["poblacion"])


def pais_menor_poblacion(paises):                                                # Devuelve el país con MENOR población. None si la lista está vacía.
    if not paises:
        return None
    return min(paises, key=lambda p: p["poblacion"])


def promedio_poblacion(paises):                                                  # Devuelve el promedio de población. 0 si la lista está vacía. 
    if not paises:
        return 0
    return sum(p["poblacion"] for p in paises) / len(paises)


def promedio_superficie(paises):                                                 # Devuelve el promedio de superficie. 0 si la lista está vacía. 
    if not paises:
        return 0
    return sum(p["superficie"] for p in paises) / len(paises)


def cantidad_por_continente(paises):                                             # Devuelve un diccionario {continente: cantidad}, recorre la lista una sola vez sumando contadores y ordena el resultadopor cantidad descendente para hacer la salida más legible.    
    conteo = {}
    for p in paises:
        cont = p["continente"]
        conteo[cont] = conteo.get(cont, 0) + 1

    return dict(sorted(conteo.items(), key=lambda kv: kv[1], reverse=True))

def mostrar_estadisticas(paises):                                                # Imprime todas las estadísticas requeridas por la consigna.
    if not paises:
        print("\n  No hay países cargados para calcular estadísticas.")
        return

    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)
    prom_pob = promedio_poblacion(paises)
    prom_sup = promedio_superficie(paises)
    por_cont = cantidad_por_continente(paises)

    print("\n=== Estadísticas del dataset ===")
    print(f"  Total de países cargados: {len(paises)}")
    print(f"\n  País con MAYOR población: {mayor['nombre']} ({mayor['poblacion']:,} habitantes)")
    print(f"  País con MENOR población: {menor['nombre']} ({menor['poblacion']:,} habitantes)")
    print(f"\n  Promedio de población : {prom_pob:>20,.2f} habitantes")
    print(f"  Promedio de superficie: {prom_sup:>20,.2f} km²")
    print("\n  Cantidad de países por continente:")
    for cont, cant in por_cont.items():
        print(f"    {cont:<12}: {cant} países")
