"""
path: src/infrastructure/settings/config.py
"""

from decimal import Decimal
from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.entities.listado_precios import ListadoPrecios
from src.entities.mix_ventas import MixVentas
from src.infrastructure.google_sheets.escenario_gateway import (
    GoogleSheetsEscenarioConfig,
    GoogleSheetsEscenarioGateway,
    ProductoSheetKey,
)
from src.infrastructure.settings.logger import get_logger
from src.use_cases import CalcularPuntoEquilibrioInput

def _load_env_file_fallback() -> None:
    """
    Carga minima de .env para casos donde python-dotenv no esta instalado.
    Formato soportado: KEY=VALUE por linea, ignorando comentarios.
    """
    env_path = ".env"
    try:
        with open(env_path, "r", encoding="utf-8") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", maxsplit=1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        return


if load_dotenv is not None:
    load_dotenv()
else:
    _load_env_file_fallback()

logger = get_logger(__name__)

USE_GOOGLE_SHEETS = True
ESCENARIO_SOURCE = "google_sheets" if USE_GOOGLE_SHEETS else "config"
GOOGLE_SHEETS_SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1-Mge959dZNJ2F6M5irEJoRKhsymCZmh8bDwyLWAitwM/edit?usp=sharing"
)
GOOGLE_SHEETS_MIX_RANGE = "'POR BOLSA X MES'!A2:AR"
GOOGLE_SHEETS_PRODUCT_KEYS = (
    "120819 MARRON:120819,MARRON;"
    "221030 MARRON:221030,MARRON;"
    "301241 MARRON:301241,MARRON"
)


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
    productos=("120819 MARRON", "221030 MARRON", "301241 MARRON"),
    cf=COSTO_FIJO_MENSUAL,
    pv=LISTADO_PRECIOS_MENSUAL,
    cv=COSTOS_VARIABLES_MENSUALES,
    m=MIX_VENTAS_MENSUAL,
)


class ConfigEscenarioGateway:  # pylint: disable=too-few-public-methods
    "Implementacion de gateway que provee escenario desde config local."

    def __init__(self) -> None:
        self._source = ESCENARIO_SOURCE.strip().lower()
        logger.debug("ConfigEscenarioGateway source=%s", self._source)

    def _obtener_desde_google_sheets(self) -> CalcularPuntoEquilibrioInput:
        spreadsheet_url = GOOGLE_SHEETS_SPREADSHEET_URL
        service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()
        mix_range = GOOGLE_SHEETS_MIX_RANGE
        keys_raw = GOOGLE_SHEETS_PRODUCT_KEYS.strip()
        logger.info("Fuente de escenario: google_sheets")
        logger.debug("Spreadsheet URL/ID: %s", spreadsheet_url)
        logger.debug("Mix range: %s", mix_range)
        logger.debug("Product keys raw: %s", keys_raw)

        if not service_account_file:
            raise ValueError(
                "Falta GOOGLE_SERVICE_ACCOUNT_FILE para usar ESCENARIO_SOURCE=google_sheets."
            )

        product_keys = self._parse_product_keys(keys_raw)
        logger.debug("Product keys parseadas: %s", product_keys)
        if len(product_keys) != len(ESCENARIO_BASE.productos):
            raise ValueError(
                "La cantidad de GOOGLE_SHEETS_PRODUCT_KEYS debe coincidir con "
                "la cantidad de productos en config local."
            )

        gateway = GoogleSheetsEscenarioGateway(
            config=GoogleSheetsEscenarioConfig(
                spreadsheet_url_or_id=spreadsheet_url,
                service_account_file=service_account_file,
                mix_range=mix_range,
            )
        )
        mix = gateway.obtener_mix_ventas_por_claves(product_keys=product_keys)
        logger.info("Mix obtenido desde Google Sheets.")
        logger.debug("Mix remoto final: %s", mix.as_tuple())
        return CalcularPuntoEquilibrioInput(
            cf=ESCENARIO_BASE.cf,
            productos=list(ESCENARIO_BASE.productos),
            pv=ESCENARIO_BASE.pv,
            cv=ESCENARIO_BASE.cv,
            m=mix,
        )

    @staticmethod
    def _parse_product_keys(raw: str) -> tuple[ProductoSheetKey, ...]:
        """
        Formato:
        120819 MARRON:120819,MARRON;221030 MARRON:221030,MARRON;301241 MARRON:301241,MARRON
        """
        entries = [entry.strip() for entry in raw.split(";") if entry.strip()]
        parsed: list[ProductoSheetKey] = []
        for entry in entries:
            if ":" not in entry:
                raise ValueError(
                    "Formato invalido en GOOGLE_SHEETS_PRODUCT_KEYS. Falta ':'."
                )
            producto, key_part = entry.split(":", maxsplit=1)
            if "," not in key_part:
                raise ValueError(
                    "Formato invalido en GOOGLE_SHEETS_PRODUCT_KEYS. Falta ','."
                )
            modelo, papel = [piece.strip() for piece in key_part.split(",", maxsplit=1)]
            parsed.append(
                ProductoSheetKey(
                    producto=producto.strip(),
                    modelo=modelo,
                    papel=papel,
                )
            )
        if not parsed:
            raise ValueError("GOOGLE_SHEETS_PRODUCT_KEYS no puede estar vacio.")
        return tuple(parsed)

    def obtener_escenario_base(self) -> CalcularPuntoEquilibrioInput:
        if self._source == "google_sheets":
            return self._obtener_desde_google_sheets()

        logger.info("Fuente de escenario: config local")
        logger.debug("Mix local: %s", ESCENARIO_BASE.m.as_tuple())
        return CalcularPuntoEquilibrioInput(
            cf=ESCENARIO_BASE.cf,
            productos=list(ESCENARIO_BASE.productos),
            pv=ESCENARIO_BASE.pv,
            cv=ESCENARIO_BASE.cv,
            m=ESCENARIO_BASE.m,
        )
