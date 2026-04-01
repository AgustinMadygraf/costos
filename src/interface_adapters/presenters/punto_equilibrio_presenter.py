"""
Path: src/interface_adapters/presenters/punto_equilibrio_presenter.py
"""

from src.infrastructure.settings.logger import get_logger


logger = get_logger(__name__)


def imprimir_resultados(resultado):
    "Presenta los resultados del calculo de punto de equilibrio de forma legible."
    productos = resultado["productos"]
    cf = resultado["cf"]
    pv = resultado["pv"]
    cv = resultado["cv"]
    m = resultado["m"]
    mc = resultado["mc"]
    mc_promedio = resultado["mc_promedio"]
    q_e_total = resultado["q_e_total"]
    q_e = resultado["q_e"]
    ventas_eq = resultado["ventas_eq"]
    costos_variables_eq = resultado["costos_variables_eq"]
    contribucion_eq = resultado["contribucion_eq"]

    logger.info("=== PARAMETROS DE ENTRADA ===")
    logger.info("CF total: %s", format(cf, ",.2f"))

    logger.info("=== DATOS POR PRODUCTO ===")
    for i, prod in enumerate(productos):
        logger.info(
            "%s: PV=%s | CV=%s | MC=%s | Mix=%s",
            prod,
            format(pv[i], ",.2f"),
            format(cv[i], ",.2f"),
            format(mc[i], ",.2f"),
            format(m[i], ".4f"),
        )

    logger.info("=== RESULTADOS ===")
    logger.info(
        "Margen promedio ponderado del mix: %s",
        format(mc_promedio, ",.4f"),
    )
    logger.info(
        "Punto de equilibrio total (q_e_total): %s unidades del mix",
        format(q_e_total, ",.4f"),
    )

    logger.info("=== VECTOR q_e (cantidades por producto en equilibrio) ===")
    for i, prod in enumerate(productos):
        logger.info(
            "%s: q_e=%s unidades | Ventas=%s | CV total=%s | Contribucion=%s",
            prod,
            format(q_e[i], ",.4f"),
            format(ventas_eq[i], ",.2f"),
            format(costos_variables_eq[i], ",.2f"),
            format(contribucion_eq[i], ",.2f"),
        )

    logger.info("=== CONTROL ===")
    logger.info("Ventas totales en equilibrio: %s", format(ventas_eq.sum(), ",.2f"))
    logger.info(
        "Costos variables totales en equilibrio: %s",
        format(costos_variables_eq.sum(), ",.2f"),
    )
    logger.info(
        "Contribucion total en equilibrio: %s",
        format(contribucion_eq.sum(), ",.2f"),
    )
    logger.info("CF total: %s", format(cf, ",.2f"))
    logger.info(
        "Diferencia contribucion - CF: %s",
        format(contribucion_eq.sum() - cf, ",.10f"),
    )
