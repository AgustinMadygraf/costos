"""
path: src/infrastructure/settings/config.py
"""

from decimal import Decimal
from dataclasses import dataclass

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.mix_ventas import MixVentas


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

MIX_VENTAS_MENSUAL = MixVentas(valores=(0.5, 0.3, 0.2))


@dataclass(frozen=True)
class EscenarioBase:
    "Configuracion base para ejecutar el escenario principal."

    productos: tuple[str, ...]
    cf: CostoFijo
    pv: ListadoPrecios
    cv: CostosVariables
    m: MixVentas


ESCENARIO_BASE = EscenarioBase(
    productos=("Bolsa A", "Bolsa B", "Bolsa C"),
    cf=COSTO_FIJO_MENSUAL,
    pv=LISTADO_PRECIOS_MENSUAL,
    cv=COSTOS_VARIABLES_MENSUALES,
    m=MIX_VENTAS_MENSUAL,
)
