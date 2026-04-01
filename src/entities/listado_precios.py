"""
Path: src/entities/listado_precios.py
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ListadoPrecios:
    "Representa el vector de precios de venta unitarios por producto."

    valores: tuple[float, ...]
    moneda: str = "ARS"

    def __post_init__(self) -> None:
        if len(self.valores) == 0:
            raise ValueError("El vector de precios no puede estar vacio.")
        if not self.moneda.strip():
            raise ValueError("La moneda de precios no puede estar vacia.")

        vector = tuple(float(valor) for valor in self.valores)
        if any(valor < 0 for valor in vector):
            raise ValueError("Los precios no pueden ser negativos.")

        object.__setattr__(self, "valores", vector)

    def as_array(self) -> np.ndarray:
        "Retorna el vector de precios como un array de numpy."
        return np.array(self.valores, dtype=float)

    def ponderado_por_mix(self, m: np.ndarray) -> float:
        "Retorna el precio promedio ponderado por mix."
        return float(self.as_array() @ np.array(m, dtype=float))

    def total_para_volumen(self, q: np.ndarray) -> float:
        "Retorna la venta total para un vector de cantidades."
        return float(self.as_array() @ np.array(q, dtype=float))
