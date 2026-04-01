"""
Path: src/interface_adapters/gateways/escenario_gateway.py
"""

from typing import Protocol

from src.use_cases import CalcularPuntoEquilibrioInput


class EscenarioGateway(Protocol):  # pylint: disable=too-few-public-methods
    "Puerto para obtener datos de escenario de entrada."

    def obtener_escenario_base(self) -> CalcularPuntoEquilibrioInput:
        "Retorna el escenario base listo para ejecutar el caso de uso."
