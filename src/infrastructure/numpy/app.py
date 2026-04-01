"""
Path: src/infrastructure/numpy/app.py
"""

import numpy as np

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.mix_ventas import MixVentas
from src.entities.volumen_produccion import VolumenProduccion


def _normalizar_costo_fijo(cf):
    if isinstance(cf, CostoFijo):
        return float(cf.monto)
    return float(cf)


def _normalizar_costos_variables(cv):
    if isinstance(cv, CostosVariables):
        return np.array(cv.as_tuple(), dtype=float)
    return np.array(cv, dtype=float)


def _normalizar_precios_venta(pv):
    if isinstance(pv, ListadoPrecios):
        return np.array(pv.as_tuple(), dtype=float)
    return np.array(pv, dtype=float)


def _normalizar_mix_ventas(m):
    if isinstance(m, MixVentas):
        return np.array(m.as_tuple(), dtype=float)
    return np.array(m, dtype=float)


def _as_float_tuple(vector) -> tuple[float, ...]:
    "Convierte un vector a una tupla de floats, asegurando que sea un vector 1D."
    return tuple(float(valor) for valor in np.array(vector, dtype=float).tolist())


def calcular_punto_equilibrio(cf, productos, pv, cv, m):
    "Calcula el punto de equilibrio para un mix de productos usando numpy."
    productos = list(productos)
    pv = _normalizar_precios_venta(pv)
    cv = _normalizar_costos_variables(cv)
    m = _normalizar_mix_ventas(m)
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
