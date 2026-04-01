"""
Path: src/interface_adapters/controllers/punto_equilibrio_controller.py
"""

from src.use_cases import CalcularPuntoEquilibrioInput, CalcularPuntoEquilibrioUseCase


class PuntoEquilibrioController:  # pylint: disable=too-few-public-methods
    "Controller de entrada para ejecutar el caso de uso de punto de equilibrio."

    def __init__(self, use_case: CalcularPuntoEquilibrioUseCase) -> None:
        self._use_case = use_case

    def handle(self, *, cf, productos, pv, cv, m):
        "Orquesta la llamada al caso de uso con los parametros de entrada."
        data = CalcularPuntoEquilibrioInput(
            cf=cf,
            productos=productos,
            pv=pv,
            cv=cv,
            m=m,
        )
        return self._use_case.execute(data)
