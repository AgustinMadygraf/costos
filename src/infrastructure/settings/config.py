"""
path: src/infrastructure/settings/config.py
"""

from dataclasses import dataclass
from decimal import Decimal
import json
import os
from pathlib import Path

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.mix_ventas import MixVentas
from src.infrastructure.settings.logger import get_logger
from src.use_cases import CalcularPuntoEquilibrioInput

os.environ["LOG_LEVEL"] = "INFO"
logger = get_logger(__name__)

def _load_escenario_json() -> dict:
    base_dir = Path(__file__).resolve().parents[3]
    json_path = base_dir / "data" / "escenario_base.json"
    with json_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def _build_entities_from_json(payload: dict):
    moneda = str(payload["moneda"])
    cf_payload = payload["costo_fijo"]
    products_payload = payload["productos"]
    if not products_payload:
        raise ValueError("escenario_base.json invalido: productos no puede estar vacio.")

    productos = tuple(
        f"{str(item['codigo']).strip()} {str(item['color']).strip().upper()}"
        for item in products_payload
    )
    precios = tuple(float(item["pv"]) for item in products_payload)
    costos = tuple(float(item["cv"]) for item in products_payload)
    mix = tuple(float(item["mix"]) for item in products_payload)

    costo_fijo = CostoFijo(
        monto=Decimal(str(cf_payload["monto"])),
        periodo=str(cf_payload["periodo"]),
        moneda=moneda,
    )
    listado_precios = ListadoPrecios(
        valores=precios,
        moneda=moneda,
    )
    costos_variables = CostosVariables(
        valores=costos,
        moneda=moneda,
    )
    mix_ventas = MixVentas(valores=mix)
    return costo_fijo, productos, listado_precios, costos_variables, mix_ventas


_ESCENARIO_JSON = _load_escenario_json()
(
    COSTO_FIJO_MENSUAL,
    HARD_CODED_PRODUCTOS_20,
    LISTADO_PRECIOS_MENSUAL,
    COSTOS_VARIABLES_MENSUALES,
    MIX_VENTAS_MENSUAL,
) = _build_entities_from_json(_ESCENARIO_JSON)


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
