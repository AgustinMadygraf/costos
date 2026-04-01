import numpy as np
import pytest

from src.entities.listado_precios import ListadoPrecios
from src.infrastructure.numpy.app import calcular_punto_equilibrio


def test_listado_precios_no_permite_negativos():
    with pytest.raises(ValueError):
        ListadoPrecios(valores=(10, -1, 5))


def test_listado_precios_ponderado_por_mix():
    pv = ListadoPrecios(valores=(120, 150, 100))
    mix = np.array([0.5, 0.3, 0.2], dtype=float)
    assert pv.ponderado_por_mix(mix) == pytest.approx(125.0)


def test_listado_precios_total_para_volumen():
    pv = ListadoPrecios(valores=(120, 150, 100))
    q = np.array([1000, 500, 200], dtype=float)
    assert pv.total_para_volumen(q) == pytest.approx(215000.0)


def test_calculo_acepta_entidad_listado_precios():
    resultado = calcular_punto_equilibrio(
        cf=100000,
        productos=["A", "B"],
        pv=ListadoPrecios(valores=(100, 120)),
        cv=[60, 80],
        m=[0.5, 0.5],
    )
    assert np.allclose(resultado["pv"], np.array([100.0, 120.0]))
