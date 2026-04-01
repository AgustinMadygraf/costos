"""
Path: src/interface_adapters/presenters/punto_equilibrio_presenter.py
"""


def presentar_resultados(resultado):
    "Construye lineas legibles para presentar el resultado de punto de equilibrio."
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

    lineas = []
    lineas.append("=== PARAMETROS DE ENTRADA ===")
    lineas.append(f"CF total: {format(cf, ',.2f')}")

    lineas.append("=== DATOS POR PRODUCTO ===")
    for i, prod in enumerate(productos):
        lineas.append(
            (
                f"{prod}: "
                f"PV={format(pv[i], ',.2f')} | "
                f"CV={format(cv[i], ',.2f')} | "
                f"MC={format(mc[i], ',.2f')} | "
                f"Mix={format(m[i], '.4f')}"
            )
        )

    lineas.append("=== RESULTADOS ===")
    lineas.append(f"Margen promedio ponderado del mix: {format(mc_promedio, ',.4f')}")
    lineas.append(
        f"Punto de equilibrio total (q_e_total): {format(q_e_total, ',.4f')} unidades del mix"
    )

    lineas.append("=== VECTOR q_e (cantidades por producto en equilibrio) ===")
    for i, prod in enumerate(productos):
        lineas.append(
            (
                f"{prod}: "
                f"q_e={format(q_e[i], ',.4f')} unidades | "
                f"Ventas={format(ventas_eq[i], ',.2f')} | "
                f"CV total={format(costos_variables_eq[i], ',.2f')} | "
                f"Contribucion={format(contribucion_eq[i], ',.2f')}"
            )
        )

    lineas.append("=== CONTROL ===")
    lineas.append(f"Ventas totales en equilibrio: {format(ventas_eq.sum(), ',.2f')}")
    lineas.append(
        f"Costos variables totales en equilibrio: {format(costos_variables_eq.sum(), ',.2f')}"
    )
    lineas.append(
        f"Contribucion total en equilibrio: {format(contribucion_eq.sum(), ',.2f')}"
    )
    lineas.append(f"CF total: {format(cf, ',.2f')}")
    lineas.append(
        f"Diferencia contribucion - CF: {format(contribucion_eq.sum() - cf, ',.10f')}"
    )

    return lineas
