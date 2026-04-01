from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CostosVariables:
    """
    Representa el vector de costos variables unitarios por producto.
    """

    valores: tuple[float, ...]
    moneda: str = "ARS"

    def __post_init__(self) -> None:
        if len(self.valores) == 0:
            raise ValueError("El vector de costos variables no puede estar vacio.")
        if not self.moneda.strip():
            raise ValueError("La moneda de costos variables no puede estar vacia.")

        vector = tuple(float(valor) for valor in self.valores)
        if any(valor < 0 for valor in vector):
            raise ValueError("Los costos variables no pueden ser negativos.")

        object.__setattr__(self, "valores", vector)

    def as_array(self) -> np.ndarray:
        return np.array(self.valores, dtype=float)

    def ponderado_por_mix(self, m: np.ndarray) -> float:
        """
        Retorna el costo variable promedio ponderado por mix.
        """
        return float(self.as_array() @ np.array(m, dtype=float))

    def total_para_volumen(self, q: np.ndarray) -> float:
        """
        Retorna el costo variable total para un vector de cantidades.
        """
        return float(self.as_array() @ np.array(q, dtype=float))
