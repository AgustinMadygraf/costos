"""
Path: src/main_mix.py
"""

from src.infrastructure.settings import ConfigEscenarioGateway, configure_logging, get_logger


logger = get_logger(__name__)


def main() -> None:
    "Entrypoint para mostrar solo el mix de ventas."
    configure_logging()
    logger.debug("Iniciando entrypoint de mix de ventas.")
    escenario = ConfigEscenarioGateway().obtener_escenario_base()
    logger.debug("Escenario cargado con %s productos.", len(escenario.productos))

    logger.info("=== MIX DE VENTAS ===")
    for producto, peso in zip(escenario.productos, escenario.m.as_tuple()):
        logger.info("%s: Mix=%.4f", producto, peso)
        logger.debug("Detalle mix | producto=%s | peso=%s", producto, peso)
    logger.info("Suma mix: %.10f", sum(escenario.m.as_tuple()))
    logger.debug("Vector final de mix: %s", escenario.m.as_tuple())


if __name__ == "__main__":
    main()
