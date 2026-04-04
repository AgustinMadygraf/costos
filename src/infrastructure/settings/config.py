"""
path: src/infrastructure/settings/config.py
"""

from dataclasses import dataclass
from decimal import Decimal
import os

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.mix_ventas import MixVentas
from src.infrastructure.settings.logger import get_logger
from src.use_cases import CalcularPuntoEquilibrioInput

os.environ["LOG_LEVEL"] = "INFO"
logger = get_logger(__name__)

COSTO_FIJO_MENSUAL = CostoFijo(
    monto=Decimal("100000.00"),
    periodo="mensual",
    moneda="ARS",
)

HARD_CODED_PRODUCTOS_20 = (
    "120819 BLANCO",
    "120819 MARRON",
    "120826 BLANCO",
    "120826 MARRON",
    "120841 BLANCO",
    "120841 MARRON",
    "161024 MARRON",
    "221020 MARRON",
    "221030 BLANCO",
    "221030 MARRON",
    "221041 BLANCO",
    "221041 MARRON",
    "261236 BLANCO",
    "261236 MARRON",
    "281638 BLANCO",
    "281638 MARRON",
    "301232 BLANCO",
    "301232 MARRON",
    "301241 BLANCO",
    "301241 MARRON",
)

LISTADO_PRECIOS_MENSUAL = ListadoPrecios(
    valores=(
        115.0,
        120.0,
        115.0,
        120.0,
        115.0,
        120.0,
        120.0,
        120.0,
        115.0,
        150.0,
        115.0,
        120.0,
        115.0,
        120.0,
        115.0,
        120.0,
        115.0,
        120.0,
        115.0,
        100.0,
    ),
    moneda="ARS",
)

COSTOS_VARIABLES_MENSUALES = CostosVariables(
    valores=(
        68.0,
        70.0,
        68.0,
        70.0,
        68.0,
        70.0,
        70.0,
        70.0,
        68.0,
        90.0,
        68.0,
        70.0,
        68.0,
        70.0,
        68.0,
        70.0,
        68.0,
        70.0,
        68.0,
        60.0,
    ),
    moneda="ARS",
)

MIX_VENTAS_MENSUAL = MixVentas(
    valores=(
        0.005684282958,
        0.130663714828,
        0.000747931968,
        0.005265441055,
        0.002842141479,
        0.059460591465,
        0.166564449298,
        0.001495863936,
        0.070156018609,
        0.217842665031,
        0.002393382298,
        0.024577044472,
        0.020343749533,
        0.100507097874,
        0.001495863936,
        0.006388834872,
        0.003590073447,
        0.047194507188,
        0.010919806734,
        0.121866539020,
    )
)


@dataclass(frozen=True)
class EscenarioBase:
    "Configuracion base hardcodeada del escenario principal."

    productos: tuple[str, ...]
    cf: CostoFijo
    pv: ListadoPrecios
    cv: CostosVariables
    m: MixVentas


ESCENARIO_BASE = EscenarioBase(
    productos=HARD_CODED_PRODUCTOS_20,
    cf=COSTO_FIJO_MENSUAL,
    pv=LISTADO_PRECIOS_MENSUAL,
    cv=COSTOS_VARIABLES_MENSUALES,
    m=MIX_VENTAS_MENSUAL,
)


class ConfigEscenarioGateway:  # pylint: disable=too-few-public-methods
    "Gateway de escenario con valores hardcodeados."

    def obtener_escenario_base(self) -> CalcularPuntoEquilibrioInput:
        logger.info("Fuente de escenario: hardcoded")
        return CalcularPuntoEquilibrioInput(
            cf=ESCENARIO_BASE.cf,
            productos=list(ESCENARIO_BASE.productos),
            pv=ESCENARIO_BASE.pv,
            cv=ESCENARIO_BASE.cv,
            m=ESCENARIO_BASE.m,
        )
