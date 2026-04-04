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
    moneda = str(payload.get("moneda") or "ARS")
    cf_payload = payload.get("costo_fijo") or {}

    products_mix = payload.get("productos_mix") or []
    products_pv = payload.get("productos_pv") or []
    products_cv = payload.get("productos_cv") or []
    if not products_mix:
        raise ValueError(
            "escenario_base.json invalido: productos_mix no puede estar vacio."
        )

    # Fallbacks para permitir placeholders null en JSON mientras se completan datos.
    default_pv_by_key = {
        ("120819", "BLANCO"): 115.0,
        ("120819", "MARRON"): 120.0,
        ("120826", "BLANCO"): 115.0,
        ("120826", "MARRON"): 120.0,
        ("120841", "BLANCO"): 115.0,
        ("120841", "MARRON"): 120.0,
        ("161024", "MARRON"): 120.0,
        ("221020", "MARRON"): 120.0,
        ("221030", "BLANCO"): 115.0,
        ("221030", "MARRON"): 150.0,
        ("221041", "BLANCO"): 115.0,
        ("221041", "MARRON"): 120.0,
        ("261236", "BLANCO"): 115.0,
        ("261236", "MARRON"): 120.0,
        ("281638", "BLANCO"): 115.0,
        ("281638", "MARRON"): 120.0,
        ("301232", "BLANCO"): 115.0,
        ("301232", "MARRON"): 120.0,
        ("301241", "BLANCO"): 115.0,
        ("301241", "MARRON"): 100.0,
    }
    default_cv_by_key = {
        ("120819", "BLANCO"): 68.0,
        ("120819", "MARRON"): 70.0,
        ("120826", "BLANCO"): 68.0,
        ("120826", "MARRON"): 70.0,
        ("120841", "BLANCO"): 68.0,
        ("120841", "MARRON"): 70.0,
        ("161024", "MARRON"): 70.0,
        ("221020", "MARRON"): 70.0,
        ("221030", "BLANCO"): 68.0,
        ("221030", "MARRON"): 90.0,
        ("221041", "BLANCO"): 68.0,
        ("221041", "MARRON"): 70.0,
        ("261236", "BLANCO"): 68.0,
        ("261236", "MARRON"): 70.0,
        ("281638", "BLANCO"): 68.0,
        ("281638", "MARRON"): 70.0,
        ("301232", "BLANCO"): 68.0,
        ("301232", "MARRON"): 70.0,
        ("301241", "BLANCO"): 68.0,
        ("301241", "MARRON"): 60.0,
    }

    pv_by_key: dict[tuple[str, str, str], float] = {}
    for item in products_pv:
        key = (
            str(item["codigo"]).strip(),
            str(item["color"]).strip().upper(),
            str(item.get("tipo_bolsa") or "CON_MANIJA").strip().upper(),
        )
        pv_value = item.get("pv")
        if pv_value is not None:
            pv_by_key[key] = float(pv_value)

    cv_by_key: dict[tuple[str, str, str], float] = {}
    for item in products_cv:
        key = (
            str(item["codigo"]).strip(),
            str(item["color"]).strip().upper(),
            str(item.get("tipo_bolsa") or "CON_MANIJA").strip().upper(),
        )
        cv_value = item.get("cv")
        if cv_value is not None:
            cv_by_key[key] = float(cv_value)

    productos_list: list[str] = []
    precios_list: list[float] = []
    costos_list: list[float] = []
    mix_list: list[float] = []
    for item in products_mix:
        codigo = str(item["codigo"]).strip()
        color = str(item["color"]).strip().upper()
        tipo_bolsa = str(item.get("tipo_bolsa") or "CON_MANIJA").strip().upper()
        key = (codigo, color, tipo_bolsa)
        default_key = (codigo, color)
        productos_list.append(f"{codigo} {color} {tipo_bolsa}")
        mix_list.append(float(item["mix"]))
        precios_list.append(pv_by_key.get(key, default_pv_by_key[default_key]))
        costos_list.append(cv_by_key.get(key, default_cv_by_key[default_key]))

    productos = tuple(productos_list)
    precios = tuple(precios_list)
    costos = tuple(costos_list)
    mix = tuple(mix_list)

    costo_fijo = CostoFijo(
        monto=Decimal(str(cf_payload.get("monto") or "100000.00")),
        periodo=str(cf_payload.get("periodo") or "mensual"),
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
    HARD_CODED_PRODUCTOS,
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
    productos=HARD_CODED_PRODUCTOS,
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
