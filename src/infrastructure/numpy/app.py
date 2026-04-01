import numpy as np

from src.entities.costo_fijo import CostoFijo


def _normalizar_costo_fijo(cf):
    if isinstance(cf, CostoFijo):
        return float(cf.monto)
    return float(cf)


def calcular_punto_equilibrio(cf, productos, pv, cv, m):
    productos = list(productos)
    pv = np.array(pv, dtype=float)
    cv = np.array(cv, dtype=float)
    m = np.array(m, dtype=float)
    cf = _normalizar_costo_fijo(cf)

    # Validaciones básicas
    n = len(productos)

    if not (len(pv) == len(cv) == len(m) == n):
        raise ValueError(
            "productos, pv, cv y m deben tener la misma longitud."
        )

    if cf < 0:
        raise ValueError("CF no puede ser negativo.")

    if np.any(pv < 0):
        raise ValueError("Los precios de venta no pueden ser negativos.")

    if np.any(cv < 0):
        raise ValueError("Los costos variables no pueden ser negativos.")

    if np.any(m < 0):
        raise ValueError("El mix m no puede tener valores negativos.")

    if not np.isclose(m.sum(), 1.0, atol=1e-9):
        raise ValueError(
            f"El vector m debe sumar 1. Suma actual: {m.sum():.10f}"
        )

    # Margen de contribución unitario por producto
    mc = pv - cv

    if np.any(mc <= 0):
        raise ValueError(
            "Todos los márgenes unitarios (pv - cv) deben ser mayores que 0 "
            "para que el modelo tenga sentido económico."
        )

    # Margen promedio ponderado del mix
    mc_promedio = mc @ m

    if mc_promedio <= 0:
        raise ValueError(
            "El margen promedio ponderado debe ser mayor que 0."
        )

    # Punto de equilibrio total
    Qe = cf / mc_promedio

    # Vector de cantidades por producto en equilibrio
    qe = Qe * m

    # Ventas y costos variables en equilibrio por producto
    ventas_eq = pv * qe
    costos_variables_eq = cv * qe
    contribucion_eq = mc * qe

    return {
        "productos": productos,
        "cf": cf,
        "pv": pv,
        "cv": cv,
        "m": m,
        "mc": mc,
        "mc_promedio": mc_promedio,
        "Qe": Qe,
        "qe": qe,
        "ventas_eq": ventas_eq,
        "costos_variables_eq": costos_variables_eq,
        "contribucion_eq": contribucion_eq,
    }


def imprimir_resultados(resultado):
    productos = resultado["productos"]
    cf = resultado["cf"]
    pv = resultado["pv"]
    cv = resultado["cv"]
    m = resultado["m"]
    mc = resultado["mc"]
    mc_promedio = resultado["mc_promedio"]
    Qe = resultado["Qe"]
    qe = resultado["qe"]
    ventas_eq = resultado["ventas_eq"]
    costos_variables_eq = resultado["costos_variables_eq"]
    contribucion_eq = resultado["contribucion_eq"]

    print("\n=== PARÁMETROS DE ENTRADA ===")
    print(f"CF total: {cf:,.2f}")

    print("\n=== DATOS POR PRODUCTO ===")
    for i, prod in enumerate(productos):
        print(
            f"{prod}: "
            f"PV={pv[i]:,.2f} | "
            f"CV={cv[i]:,.2f} | "
            f"MC={mc[i]:,.2f} | "
            f"Mix={m[i]:.4f}"
        )

    print("\n=== RESULTADOS ===")
    print(f"Margen promedio ponderado del mix: {mc_promedio:,.4f}")
    print(f"Punto de equilibrio total (Qe): {Qe:,.4f} unidades del mix")

    print("\n=== VECTOR qe (cantidades por producto en equilibrio) ===")
    for i, prod in enumerate(productos):
        print(
            f"{prod}: "
            f"qe={qe[i]:,.4f} unidades | "
            f"Ventas={ventas_eq[i]:,.2f} | "
            f"CV total={costos_variables_eq[i]:,.2f} | "
            f"Contribución={contribucion_eq[i]:,.2f}"
        )

    print("\n=== CONTROL ===")
    print(f"Ventas totales en equilibrio: {ventas_eq.sum():,.2f}")
    print(f"Costos variables totales en equilibrio: {costos_variables_eq.sum():,.2f}")
    print(f"Contribución total en equilibrio: {contribucion_eq.sum():,.2f}")
    print(f"CF total: {cf:,.2f}")
    print(
        "Diferencia contribución - CF: "
        f"{contribucion_eq.sum() - cf:,.10f}"
    )
