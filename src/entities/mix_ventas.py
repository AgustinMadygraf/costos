"""
Path: src/entities/mix_ventas.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MixVentas:
    "Representa el vector de mix de ventas por producto."

    valores: tuple[float, ...]
    tolerancia_suma: float = 1e-9

    def __post_init__(self) -> None:
        if len(self.valores) == 0:
            raise ValueError("El vector de mix de ventas no puede estar vacio.")

        vector = tuple(float(valor) for valor in self.valores)
        if any(valor < 0 for valor in vector):
            raise ValueError("El mix de ventas no puede tener valores negativos.")
        if abs(sum(vector) - 1.0) > self.tolerancia_suma:
            raise ValueError(
                f"El vector de mix de ventas debe sumar 1. Suma actual: {sum(vector):.10f}"
            )

        object.__setattr__(self, "valores", vector)

    def as_tuple(self) -> tuple[float, ...]:
        "Retorna el mix como tupla de float (sin dependencias externas)."
        return self.valores
