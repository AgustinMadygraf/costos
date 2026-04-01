"""
Path: src/infrastructure/pdfplumber/extractor.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pdfplumber


def _normalizar_celda(valor: object) -> str:
    if valor is None:
        return ""
    texto = str(valor).replace("\n", " ").strip()
    return " ".join(texto.split())


def _tabla_a_markdown(tabla: Iterable[Iterable[object]]) -> str:
    filas = [[_normalizar_celda(celda) for celda in fila] for fila in tabla]
    if not filas:
        return ""

    ancho = max(len(fila) for fila in filas)
    filas = [fila + [""] * (ancho - len(fila)) for fila in filas]

    encabezado = filas[0]
    separador = ["---"] * ancho
    lineas = [
        "| " + " | ".join(encabezado) + " |",
        "| " + " | ".join(separador) + " |",
    ]
    for fila in filas[1:]:
        lineas.append("| " + " | ".join(fila) + " |")
    return "\n".join(lineas)


def extraer_tablas_pdf(ruta_pdf: str | Path) -> list[list[list[object]]]:
    ruta = Path(ruta_pdf)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el PDF: {ruta}")

    tablas: list[list[list[object]]] = []
    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            for tabla in pagina.extract_tables():
                if tabla:
                    tablas.append(tabla)
    return tablas


def extraer_tabla_markdown(
    ruta_pdf: str | Path,
    indice_tabla: int = 0,
) -> str:
    tablas = extraer_tablas_pdf(ruta_pdf)
    if not tablas:
        raise ValueError("No se detectaron tablas en el PDF.")
    if indice_tabla < 0 or indice_tabla >= len(tablas):
        raise IndexError(
            f"indice_tabla fuera de rango: {indice_tabla}. "
            f"Tablas detectadas: {len(tablas)}"
        )
    return _tabla_a_markdown(tablas[indice_tabla])
