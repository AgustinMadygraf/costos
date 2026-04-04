from src.infrastructure.settings import ConfigEscenarioGateway
from src.infrastructure.settings.config import ESCENARIO_BASE


def test_config_escenario_gateway_devuelve_escenario_hardcodeado():
    gateway = ConfigEscenarioGateway()
    data = gateway.obtener_escenario_base()

    assert data.cf == ESCENARIO_BASE.cf
    assert data.productos == list(ESCENARIO_BASE.productos)
    assert data.pv == ESCENARIO_BASE.pv
    assert data.cv == ESCENARIO_BASE.cv
    assert data.m == ESCENARIO_BASE.m


def test_config_escenario_gateway_hardcodeado_tiene_20_productos():
    gateway = ConfigEscenarioGateway()
    data = gateway.obtener_escenario_base()

    assert len(data.productos) == 20
    assert len(data.pv.as_tuple()) == 20
    assert len(data.cv.as_tuple()) == 20
    assert len(data.m.as_tuple()) == 20
