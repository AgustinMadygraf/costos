import logging

import pytest

from src.entities.costo_fijo import CostoFijo
from src.entities.costos_variables import CostosVariables
from src.infrastructure.numpy.app import calcular_punto_equilibrio
from src.interface_adapters.presenters import imprimir_resultados


def _base_kwargs():
    return {
        "cf": 100000,
        "productos": ["A", "B"],
        "pv": [100, 120],
        "cv": [60, 80],
        "m": [0.5, 0.5],
    }


@pytest.mark.parametrize(
    ("field", "value", "error_text"),
    [
        ("pv", [100], "misma longitud"),
        ("cf", -1, "CF no puede ser negativo"),
        ("pv", [-1, 120], "precios de venta"),
        ("cv", [-1, 80], "costos variables"),
        ("m", [-0.1, 1.1], "mix m"),
        ("m", [0.4, 0.5], "debe sumar 1"),
        ("pv", [60, 80], "margenes unitarios"),
    ],
)
def test_calcular_punto_equilibrio_valida_errores(field, value, error_text):
    kwargs = _base_kwargs()
    kwargs[field] = value
    with pytest.raises(ValueError, match=error_text):
        calcular_punto_equilibrio(**kwargs)


def test_calcular_punto_equilibrio_acepta_entidades_de_dominio():
    resultado = calcular_punto_equilibrio(
        cf=CostoFijo(monto="100000.00"),
        productos=["A", "B"],
        pv=[100, 120],
        cv=CostosVariables(valores=(60, 80)),
        m=[0.5, 0.5],
    )
    assert resultado["q_e_total"] == pytest.approx(resultado["q_e"].sum())


def test_imprimir_resultados_loguea_resumen(caplog):
    resultado = calcular_punto_equilibrio(**_base_kwargs())

    with caplog.at_level(logging.INFO):
        imprimir_resultados(resultado)

    mensajes = [record.getMessage() for record in caplog.records]
    assert "=== PARAMETROS DE ENTRADA ===" in mensajes
    assert any("Punto de equilibrio total (q_e_total)" in msg for msg in mensajes)
    assert any("VECTOR q_e" in msg for msg in mensajes)
