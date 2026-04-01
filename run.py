"""
Path: run.py
"""


from src.infrastructure.numpy.app import calcular_punto_equilibrio, imprimir_resultados
from src.infrastructure.settings.config import (
    COSTO_FIJO_MENSUAL,
    COSTOS_VARIABLES_MENSUALES,
    LISTADO_PRECIOS_MENSUAL,
    MIX_VENTAS_MENSUAL,
)
from src.use_cases import CalcularPuntoEquilibrioInput, CalcularPuntoEquilibrioUseCase




productos = ["Bolsa A", "Bolsa B", "Bolsa C"]

pv = LISTADO_PRECIOS_MENSUAL  # precios de venta unitarios hardcodeados
cv = COSTOS_VARIABLES_MENSUALES  # costos variables unitarios hardcodeados
m = MIX_VENTAS_MENSUAL  # mix de ventas hardcodeado (debe sumar 1)
cf = COSTO_FIJO_MENSUAL   # costos fijos totales hardcodeados

use_case = CalcularPuntoEquilibrioUseCase(calculator=calcular_punto_equilibrio)

resultado = use_case.execute(
    CalcularPuntoEquilibrioInput(
        cf=cf,
        productos=productos,
        pv=pv,
        cv=cv,
        m=m,
    )
)

imprimir_resultados(resultado)
