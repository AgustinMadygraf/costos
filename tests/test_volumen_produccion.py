"""
Path: tests/test_volumen_produccion.py
"""

import numpy as np
import pytest

from src.entities.volumen_produccion import VolumenProduccion
from src.infrastructure.numpy.app import calcular_punto_equilibrio


def test_volumen_produccion_valida_qr_menor_igual_qm():
    with pytest.raises(ValueError):
        VolumenProduccion(
            q_e=(100, 200),
            q_r=(120, 210),
            q_m=(130, 205),
        )


def test_volumen_produccion_calcula_escalas():
    volumen = VolumenProduccion(
        q_e=(100, 200),
        q_r=(90, 180),
        q_m=(120, 220),
    )
    assert volumen.q_e_total == pytest.approx(300.0)
    assert volumen.q_r_total == pytest.approx(270.0)
    assert volumen.q_m_total == pytest.approx(340.0)


def test_calculo_expone_qe_y_qe_total_canonicos():
    resultado = calcular_punto_equilibrio(
        cf=100000,
        productos=["A", "B"],
        pv=[100, 120],
        cv=[60, 80],
        m=[0.5, 0.5],
    )

    assert resultado["q_e_total"] == pytest.approx(resultado["q_e_total"].sum())
