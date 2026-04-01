import numpy as np
import pytest

from src.entities.costos_variables import CostosVariables
from src.infrastructure.numpy.app import calcular_punto_equilibrio


def test_costos_variables_no_permite_negativos():
    with pytest.raises(ValueError):
        CostosVariables(valores=(10, -1, 5))


def test_costos_variables_ponderado_por_mix():
    cv = CostosVariables(valores=(70, 90, 60))
    mix = np.array([0.5, 0.3, 0.2], dtype=float)
    assert cv.ponderado_por_mix(mix) == pytest.approx(74.0)


def test_costos_variables_total_para_volumen():
    cv = CostosVariables(valores=(70, 90, 60))
    q = np.array([1000, 500, 200], dtype=float)
    assert cv.total_para_volumen(q) == pytest.approx(127000.0)


def test_calculo_acepta_entidad_costos_variables():
    resultado = calcular_punto_equilibrio(
        cf=100000,
        productos=["A", "B"],
        pv=[100, 120],
        cv=CostosVariables(valores=(60, 80)),
        m=[0.5, 0.5],
    )
    assert np.allclose(resultado["cv"], np.array([60.0, 80.0]))
    assert resultado["Q"] == pytest.approx(resultado["qe"].sum())
    assert np.allclose(resultado["q"], resultado["qe"])
