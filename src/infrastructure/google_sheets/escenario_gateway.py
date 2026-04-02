"""
Gateway de escenario alimentado por Google Sheets API.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.entities.mix_ventas import MixVentas
from src.infrastructure.google_sheets.client import (
    GoogleSheetsReader,
    build_sheets_service,
    extract_spreadsheet_id,
)
from src.infrastructure.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class GoogleSheetsEscenarioConfig:
    spreadsheet_url_or_id: str
    service_account_file: str
    mix_range: str = "'POR BOLSA X MES'!A2:AR"


@dataclass(frozen=True)
class ProductoSheetKey:
    producto: str
    modelo: str
    papel: str


class GoogleSheetsEscenarioGateway:  # pylint: disable=too-few-public-methods
    "Lee escenario comercial desde Google Sheets."

    def __init__(
        self,
        config: GoogleSheetsEscenarioConfig,
        reader: GoogleSheetsReader | None = None,
    ) -> None:
        self._config = config
        if reader is None:
            service = build_sheets_service(config.service_account_file)
            spreadsheet_id = extract_spreadsheet_id(config.spreadsheet_url_or_id)
            reader = GoogleSheetsReader(spreadsheet_id=spreadsheet_id, service=service)
        self._reader = reader

    @staticmethod
    def _parse_number(raw: str) -> float:
        value = raw.strip()
        if not value:
            return 0.0
        normalized = value.replace(".", "").replace(",", ".")
        return float(normalized)

    def obtener_mix_ventas_por_claves(
        self, product_keys: tuple[ProductoSheetKey, ...]
    ) -> MixVentas:
        logger.info("Leyendo mix desde Google Sheets.")
        logger.debug("Range consultado: %s", self._config.mix_range)
        rows = self._reader.read_range(self._config.mix_range)
        if len(rows) < 2:
            raise ValueError(
                "No hay suficientes filas en Google Sheets para calcular mix."
            )

        header = [cell.strip() for cell in rows[0]]
        logger.debug("Header detectado: %s", header)
        try:
            col_2026 = header.index("2026")
        except ValueError as exc:
            raise ValueError(
                "No se encontro columna '2026' en la pestaña POR BOLSA X MES."
            ) from exc
        logger.debug("Indice columna 2026: %s", col_2026)

        totals_by_key: dict[tuple[str, str], float] = {}
        for row in rows[1:]:
            if len(row) < 2:
                continue
            modelo = row[0].strip()
            papel = row[1].strip() if len(row) > 1 else ""
            if not modelo and not papel:
                continue
            total = self._parse_number(row[col_2026]) if col_2026 < len(row) else 0.0
            totals_by_key[(modelo.upper(), papel.upper())] = total
        logger.debug("Totales indexados por MODELO+PAPEL: %s", totals_by_key)

        selected: list[float] = []
        for key in product_keys:
            lookup_key = (key.modelo.strip().upper(), key.papel.strip().upper())
            if lookup_key not in totals_by_key:
                raise ValueError(
                    "No se encontro MODELO+PAPEL en Google Sheets: "
                    f"{key.modelo}+{key.papel}."
                )
            selected_value = totals_by_key[lookup_key]
            selected.append(selected_value)
            logger.debug(
                "Match key=%s/%s -> total_2026=%s",
                key.modelo,
                key.papel,
                selected_value,
            )

        total_selected = sum(selected)
        if total_selected <= 0:
            raise ValueError(
                "La suma de totales 2026 seleccionados debe ser mayor a 0."
            )
        logger.debug("Suma de totales seleccionados: %s", total_selected)

        normalized_mix = tuple(value / total_selected for value in selected)
        logger.info("Mix normalizado calculado desde Google Sheets.")
        logger.debug("Mix normalizado: %s", normalized_mix)
        return MixVentas(valores=normalized_mix)
