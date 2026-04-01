from src.infrastructure.settings import ConfigEscenarioGateway
from src.infrastructure.settings.config import ESCENARIO_BASE


def test_config_escenario_gateway_devuelve_input_esperado():
    gateway = ConfigEscenarioGateway()

    data = gateway.obtener_escenario_base()

    assert data.cf == ESCENARIO_BASE.cf
    assert data.productos == list(ESCENARIO_BASE.productos)
    assert data.pv == ESCENARIO_BASE.pv
    assert data.cv == ESCENARIO_BASE.cv
    assert data.m == ESCENARIO_BASE.m
