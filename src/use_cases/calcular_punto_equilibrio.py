"""
Path: src/use_cases/calcular_punto_equilibrio.py
"""

from dataclasses import dataclass
from typing import Any, Callable


PuntoEquilibrioCalculator = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class CalcularPuntoEquilibrioInput:
    "Datos de entrada para el calculo de punto de equilibrio."

    cf: Any
    productos: list[str]
    pv: Any
    cv: Any
    m: Any


class CalcularPuntoEquilibrioUseCase:  # pylint: disable=too-few-public-methods
    "Caso de uso de aplicacion para calcular punto de equilibrio."

    def __init__(self, calculator: PuntoEquilibrioCalculator) -> None:
        self._calculator = calculator

    def execute(self, data: CalcularPuntoEquilibrioInput) -> dict[str, Any]:
        "Ejecuta el caso de uso delegando el calculo al adapter inyectado."
        return self._calculator(
            cf=data.cf,
            productos=data.productos,
            pv=data.pv,
            cv=data.cv,
            m=data.m,
        )
