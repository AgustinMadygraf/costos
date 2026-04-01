"""
Path: src/main.py
"""

import logging

from src.infrastructure.numpy.app import calcular_punto_equilibrio
from src.infrastructure.settings.config import ESCENARIO_BASE
from src.infrastructure.settings.logger import configure_logging
from src.interface_adapters.controllers import PuntoEquilibrioController
from src.interface_adapters.presenters import presentar_resultados
from src.use_cases import CalcularPuntoEquilibrioUseCase


logger = logging.getLogger(__name__)


def main() -> None:
    "Composition root de la aplicacion."
    configure_logging()

    use_case = CalcularPuntoEquilibrioUseCase(calculator=calcular_punto_equilibrio)
    controller = PuntoEquilibrioController(use_case=use_case)

    resultado = controller.handle(
        cf=ESCENARIO_BASE.cf,
        productos=list(ESCENARIO_BASE.productos),
        pv=ESCENARIO_BASE.pv,
        cv=ESCENARIO_BASE.cv,
        m=ESCENARIO_BASE.m,
    )

    for linea in presentar_resultados(resultado):
        logger.info(linea)


if __name__ == "__main__":
    main()
