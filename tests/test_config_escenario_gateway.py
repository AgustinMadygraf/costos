from src.infrastructure.settings import ConfigEscenarioGateway
import src.infrastructure.settings.config as config_module
from src.infrastructure.settings.config import ESCENARIO_BASE


def test_config_escenario_gateway_devuelve_input_esperado(monkeypatch):
    monkeypatch.setattr(config_module, "ESCENARIO_SOURCE", "config")
    gateway = ConfigEscenarioGateway()

    data = gateway.obtener_escenario_base()

    assert data.cf == ESCENARIO_BASE.cf
    assert data.productos == list(ESCENARIO_BASE.productos)
    assert data.pv == ESCENARIO_BASE.pv
    assert data.cv == ESCENARIO_BASE.cv
    assert data.m == ESCENARIO_BASE.m


def test_config_escenario_gateway_google_sheets_requiere_credenciales(monkeypatch):
    monkeypatch.setattr(config_module, "ESCENARIO_SOURCE", "google_sheets")
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_FILE", raising=False)

    gateway = ConfigEscenarioGateway()
    try:
        gateway.obtener_escenario_base()
    except ValueError as exc:
        assert "GOOGLE_SERVICE_ACCOUNT_FILE" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError por falta de credenciales.")


def test_config_escenario_gateway_google_sheets_usa_mix_remoto_y_resto_local(
    monkeypatch,
):
    class _FakeGoogleGateway:
        def __init__(self, *_args, **_kwargs):
            pass

        def obtener_mix_ventas_por_claves(self, product_keys):
            assert len(product_keys) == 3
            from src.entities.mix_ventas import MixVentas

            return MixVentas(valores=(0.2, 0.5, 0.3))

    monkeypatch.setattr(config_module, "ESCENARIO_SOURCE", "google_sheets")
    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_FILE", "fake.json")
    monkeypatch.setattr(
        "src.infrastructure.settings.config.GoogleSheetsEscenarioGateway",
        _FakeGoogleGateway,
    )

    gateway = ConfigEscenarioGateway()
    data = gateway.obtener_escenario_base()

    assert data.cf == ESCENARIO_BASE.cf
    assert data.productos == list(ESCENARIO_BASE.productos)
    assert data.pv == ESCENARIO_BASE.pv
    assert data.cv == ESCENARIO_BASE.cv
    assert data.m.as_tuple() == (0.2, 0.5, 0.3)


def test_config_escenario_gateway_valida_formato_product_keys(monkeypatch):
    monkeypatch.setattr(config_module, "ESCENARIO_SOURCE", "google_sheets")
    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_FILE", "fake.json")
    monkeypatch.setattr(config_module, "GOOGLE_SHEETS_PRODUCT_KEYS", "formato_invalido")

    gateway = ConfigEscenarioGateway()
    try:
        gateway.obtener_escenario_base()
    except ValueError as exc:
        assert "Formato invalido en GOOGLE_SHEETS_PRODUCT_KEYS" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError por formato invalido.")
