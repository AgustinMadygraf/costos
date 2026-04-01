"""
Path: src/entities/listado_precios.py
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


_TWO_DECIMALS = Decimal("0.01")


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

        vector = tuple(
            float(Decimal(str(valor)).quantize(_TWO_DECIMALS, rounding=ROUND_HALF_UP))
            for valor in self.valores
        )
        if any(valor < 0 for valor in vector):
            raise ValueError("Los precios no pueden ser negativos.")

        object.__setattr__(self, "valores", vector)

    def as_tuple(self) -> tuple[float, ...]:
        "Retorna el vector de precios como tupla de float."
        return self.valores

    def ponderado_por_mix(self, m) -> float:
        "Retorna el precio promedio ponderado por mix."
        mix = tuple(float(valor) for valor in m)
        if len(mix) != len(self.valores):
            raise ValueError("El mix debe tener la misma longitud que precios.")
        return float(sum(precio * peso for precio, peso in zip(self.valores, mix)))

    def total_para_volumen(self, q) -> float:
        "Retorna la venta total para un vector de cantidades."
        cantidades = tuple(float(valor) for valor in q)
        if len(cantidades) != len(self.valores):
            raise ValueError("El vector q debe tener la misma longitud que precios.")
        return float(sum(precio * cantidad for precio, cantidad in zip(self.valores, cantidades)))
