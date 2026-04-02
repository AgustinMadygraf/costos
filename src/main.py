"""
Path: src/main.py
"""

from src.infrastructure.numpy.app import calcular_punto_equilibrio
from src.infrastructure.settings import (
    ConfigEscenarioGateway,
    configure_logging,
    get_logger,
)
from src.interface_adapters.controllers import PuntoEquilibrioController
from src.interface_adapters.presenters import presentar_resultados
from src.use_cases import CalcularPuntoEquilibrioUseCase


logger = get_logger(__name__)


def main() -> None:
    "Composition root de la aplicacion."
    configure_logging()

    escenario_gateway = ConfigEscenarioGateway()
    use_case = CalcularPuntoEquilibrioUseCase(calculator=calcular_punto_equilibrio)
    controller = PuntoEquilibrioController(use_case=use_case)
    escenario = escenario_gateway.obtener_escenario_base()

    resultado = controller.handle(
        cf=escenario.cf,
        productos=escenario.productos,
        pv=escenario.pv,
        cv=escenario.cv,
        m=escenario.m,
    )

    for linea in presentar_resultados(resultado):
        logger.info(linea)


if __name__ == "__main__":
    main()
