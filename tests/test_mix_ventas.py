import numpy as np
import pytest

from src.entities.mix_ventas import MixVentas
from src.infrastructure.numpy.app import calcular_punto_equilibrio


def test_mix_ventas_no_permite_negativos():
    with pytest.raises(ValueError):
        MixVentas(valores=(0.5, -0.1, 0.6))


def test_mix_ventas_valida_suma_uno():
    with pytest.raises(ValueError):
        MixVentas(valores=(0.4, 0.4, 0.1))


def test_mix_ventas_as_tuple():
    mix = MixVentas(valores=(0.5, 0.3, 0.2))
    assert mix.as_tuple() == (0.5, 0.3, 0.2)


def test_calculo_acepta_entidad_mix_ventas():
    resultado = calcular_punto_equilibrio(
        cf=100000,
        productos=["A", "B"],
        pv=[100, 120],
        cv=[60, 80],
        m=MixVentas(valores=(0.5, 0.5)),
    )
    assert np.allclose(resultado["m"], np.array([0.5, 0.5]))
