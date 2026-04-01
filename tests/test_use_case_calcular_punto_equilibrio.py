from src.infrastructure.numpy.app import calcular_punto_equilibrio
from src.use_cases import CalcularPuntoEquilibrioInput, CalcularPuntoEquilibrioUseCase


def test_use_case_delega_en_calculador_inyectado():
    captured = {}

    def fake_calculator(*, cf, productos, pv, cv, m):
        captured["cf"] = cf
        captured["productos"] = productos
        captured["pv"] = pv
        captured["cv"] = cv
        captured["m"] = m
        return {"ok": True}

    use_case = CalcularPuntoEquilibrioUseCase(calculator=fake_calculator)
    data = CalcularPuntoEquilibrioInput(
        cf=1,
        productos=["A"],
        pv=[10],
        cv=[5],
        m=[1.0],
    )

    result = use_case.execute(data)

    assert result == {"ok": True}
    assert captured == {
        "cf": 1,
        "productos": ["A"],
        "pv": [10],
        "cv": [5],
        "m": [1.0],
    }


def test_use_case_con_calculador_real():
    use_case = CalcularPuntoEquilibrioUseCase(calculator=calcular_punto_equilibrio)
    data = CalcularPuntoEquilibrioInput(
        cf=100000,
        productos=["A", "B"],
        pv=[100, 120],
        cv=[60, 80],
        m=[0.5, 0.5],
    )

    result = use_case.execute(data)

    assert "q_e_total" in result
    assert "q_e" in result
