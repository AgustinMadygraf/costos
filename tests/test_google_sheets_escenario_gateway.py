import pytest

from src.infrastructure.google_sheets.escenario_gateway import (
    GoogleSheetsEscenarioConfig,
    GoogleSheetsEscenarioGateway,
    ProductoSheetKey,
)


class _FakeReader:
    def __init__(self, values_by_range):
        self._values_by_range = values_by_range

    def read_range(self, a1_range: str):
        return self._values_by_range[a1_range]


def test_google_sheets_gateway_calcula_mix_desde_columna_2026():
    cfg = GoogleSheetsEscenarioConfig(
        spreadsheet_url_or_id="dummy",
        service_account_file="unused.json",
        mix_range="'POR BOLSA X MES'!A2:AR",
    )
    reader = _FakeReader(
        {
            "'POR BOLSA X MES'!A2:AR": [
                ["MODELO", "PAPEL", "X", "2026"],
                ["120819", "MARRON", "", "50"],
                ["120826", "MARRON", "", "30"],
                ["120841", "MARRON", "", "20"],
            ]
        }
    )
    gateway = GoogleSheetsEscenarioGateway(config=cfg, reader=reader)

    mix = gateway.obtener_mix_ventas_por_claves(
        (
            ProductoSheetKey(producto="Bolsa A", modelo="120819", papel="MARRON"),
            ProductoSheetKey(producto="Bolsa B", modelo="120826", papel="MARRON"),
            ProductoSheetKey(producto="Bolsa C", modelo="120841", papel="MARRON"),
        )
    )

    assert mix.as_tuple() == (0.5, 0.3, 0.2)


def test_google_sheets_gateway_falla_sin_columna_2026():
    cfg = GoogleSheetsEscenarioConfig(
        spreadsheet_url_or_id="dummy",
        service_account_file="unused.json",
    )
    reader = _FakeReader({cfg.mix_range: [["MODELO", "PAPEL"], ["120819", "MARRON"]]})
    gateway = GoogleSheetsEscenarioGateway(config=cfg, reader=reader)

    with pytest.raises(ValueError, match="columna '2026'"):
        gateway.obtener_mix_ventas_por_claves(
            (ProductoSheetKey(producto="Bolsa A", modelo="120819", papel="MARRON"),)
        )
