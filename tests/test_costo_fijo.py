from decimal import Decimal

import pytest

from src.entities.costo_fijo import CostoFijo
from src.infrastructure.numpy.app import calcular_punto_equilibrio


def test_costo_fijo_no_permite_monto_negativo():
    with pytest.raises(ValueError):
        CostoFijo(monto=-1)


def test_costo_fijo_redondea_a_dos_decimales():
    costo = CostoFijo(monto="100000.005")
    assert costo.monto == Decimal("100000.01")


def test_calculo_acepta_entidad_costo_fijo():
    resultado = calcular_punto_equilibrio(
        cf=CostoFijo(monto=100000, periodo="mensual", moneda="ARS"),
        productos=["A", "B"],
        pv=[100, 120],
        cv=[60, 80],
        m=[0.5, 0.5],
    )

    assert resultado["cf"] == 100000.0
