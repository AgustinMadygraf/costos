"""
path: src/infrastructure/settings/config.py
"""

from decimal import Decimal

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios


COSTO_FIJO_MENSUAL = CostoFijo(
    monto=Decimal("100000.00"),
    periodo="mensual",
    moneda="ARS",
)

LISTADO_PRECIOS_MENSUAL = ListadoPrecios(
    valores=(120, 150, 100),
    moneda="ARS",
)

COSTOS_VARIABLES_MENSUALES = CostosVariables(
    valores=(70, 90, 60),
    moneda="ARS",
)

MIX_VENTAS_MENSUAL = (0.5, 0.3, 0.2)
