"""
Path: src/infrastructure/numpy/app.py
"""

import numpy as np

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.volumen_produccion import VolumenProduccion
from src.infrastructure.settings.logger import get_logger


logger = get_logger(__name__)


def _normalizar_costo_fijo(cf):
    if isinstance(cf, CostoFijo):
        return float(cf.monto)
    return float(cf)


def _normalizar_costos_variables(cv):
    if isinstance(cv, CostosVariables):
        return cv.as_array()
    return np.array(cv, dtype=float)


def _normalizar_precios_venta(pv):
    if isinstance(pv, ListadoPrecios):
        return pv.as_array()
    return np.array(pv, dtype=float)


def _as_float_tuple(vector) -> tuple[float, ...]:
    "Convierte un vector a una tupla de floats, asegurando que sea un vector 1D."
    return tuple(float(valor) for valor in np.array(vector, dtype=float).tolist())


def calcular_punto_equilibrio(cf, productos, pv, cv, m):
    "Calcula el punto de equilibrio para un mix de productos usando numpy."
    productos = list(productos)
    pv = _normalizar_precios_venta(pv)
    cv = _normalizar_costos_variables(cv)
    m = np.array(m, dtype=float)
    cf = _normalizar_costo_fijo(cf)

    # Validaciones basicas
    n = len(productos)

    if not (len(pv) == len(cv) == len(m) == n):
        raise ValueError("productos, pv, cv y m deben tener la misma longitud.")

    if cf < 0:
        raise ValueError("CF no puede ser negativo.")

    if np.any(pv < 0):
        raise ValueError("Los precios de venta no pueden ser negativos.")

    if np.any(cv < 0):
        raise ValueError("Los costos variables no pueden ser negativos.")

    if np.any(m < 0):
        raise ValueError("El mix m no puede tener valores negativos.")

    if not np.isclose(m.sum(), 1.0, atol=1e-9):
        raise ValueError(f"El vector m debe sumar 1. Suma actual: {m.sum():.10f}")

    # Margen de contribucion unitario por producto
    mc = pv - cv

    if np.any(mc <= 0):
        raise ValueError(
            "Todos los margenes unitarios (pv - cv) deben ser mayores que 0 "
            "para que el modelo tenga sentido economico."
        )

    # Margen promedio ponderado del mix
    mc_promedio = mc @ m

    if mc_promedio <= 0:
        raise ValueError("El margen promedio ponderado debe ser mayor que 0.")

    # Punto de equilibrio total
    q_e_total_formula = cf / mc_promedio

    # Vector de cantidades por producto en equilibrio
    q_e = q_e_total_formula * m
    volumen = VolumenProduccion(q_e=_as_float_tuple(q_e))
    q_e_total = volumen.q_e_total

    # Ventas y costos variables en equilibrio por producto
    ventas_eq = pv * q_e
    costos_variables_eq = cv * q_e
    contribucion_eq = mc * q_e

    return {
        "productos": productos,
        "cf": cf,
        "pv": pv,
        "cv": cv,
        "m": m,
        "mc": mc,
        "mc_promedio": mc_promedio,
        "q_e_total": q_e_total,
        "q_e": q_e,
        "ventas_eq": ventas_eq,
        "costos_variables_eq": costos_variables_eq,
        "contribucion_eq": contribucion_eq,
    }


def imprimir_resultados(resultado):
    "Imprime los resultados del calculo de punto de equilibrio de forma legible."
    productos = resultado["productos"]
    cf = resultado["cf"]
    pv = resultado["pv"]
    cv = resultado["cv"]
    m = resultado["m"]
    mc = resultado["mc"]
    mc_promedio = resultado["mc_promedio"]
    q_e_total = resultado["q_e_total"]
    q_e = resultado["q_e"]
    ventas_eq = resultado["ventas_eq"]
    costos_variables_eq = resultado["costos_variables_eq"]
    contribucion_eq = resultado["contribucion_eq"]

    logger.info("=== PARAMETROS DE ENTRADA ===")
    logger.info("CF total: %s", format(cf, ",.2f"))

    logger.info("=== DATOS POR PRODUCTO ===")
    for i, prod in enumerate(productos):
        logger.info(
            "%s: PV=%s | CV=%s | MC=%s | Mix=%s",
            prod,
            format(pv[i], ",.2f"),
            format(cv[i], ",.2f"),
            format(mc[i], ",.2f"),
            format(m[i], ".4f"),
        )

    logger.info("=== RESULTADOS ===")
    logger.info(
        "Margen promedio ponderado del mix: %s",
        format(mc_promedio, ",.4f"),
    )
    logger.info(
        "Punto de equilibrio total (q_e_total): %s unidades del mix",
        format(q_e_total, ",.4f"),
    )

    logger.info("=== VECTOR q_e (cantidades por producto en equilibrio) ===")
    for i, prod in enumerate(productos):
        logger.info(
            "%s: q_e=%s unidades | Ventas=%s | CV total=%s | Contribucion=%s",
            prod,
            format(q_e[i], ",.4f"),
            format(ventas_eq[i], ",.2f"),
            format(costos_variables_eq[i], ",.2f"),
            format(contribucion_eq[i], ",.2f"),
        )

    logger.info("=== CONTROL ===")
    logger.info("Ventas totales en equilibrio: %s", format(ventas_eq.sum(), ",.2f"))
    logger.info(
        "Costos variables totales en equilibrio: %s",
        format(costos_variables_eq.sum(), ",.2f"),
    )
    logger.info(
        "Contribucion total en equilibrio: %s",
        format(contribucion_eq.sum(), ",.2f"),
    )
    logger.info("CF total: %s", format(cf, ",.2f"))
    logger.info(
        "Diferencia contribucion - CF: %s",
        format(contribucion_eq.sum() - cf, ",.10f"),
    )
