"""
Path: src/entities/volumen_produccion.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VolumenProduccion:
    """
    Modela volumenes por producto:
    - q_e: vector de equilibrio (obligatorio)
    - q_r: vector real (opcional)
    - q_m: vector maximo por capacidad (opcional)
    """

    q_e: tuple[float, ...]
    q_r: tuple[float, ...] | None = None
    q_m: tuple[float, ...] | None = None

    def __post_init__(self) -> None:
        q_e = self._normalizar_vector(self.q_e, "q_e")
        q_r = self._normalizar_vector(self.q_r, "q_r") if self.q_r is not None else None
        q_m = self._normalizar_vector(self.q_m, "q_m") if self.q_m is not None else None

        if q_r is not None and len(q_r) != len(q_e):
            raise ValueError("q_r debe tener la misma longitud que q_e.")
        if q_m is not None and len(q_m) != len(q_e):
            raise ValueError("q_m debe tener la misma longitud que q_e.")
        if q_r is not None and q_m is not None:
            if any(real > maximo for real, maximo in zip(q_r, q_m)):
                raise ValueError("q_r no puede superar q_m por producto.")

        object.__setattr__(self, "q_e", q_e)
        object.__setattr__(self, "q_r", q_r)
        object.__setattr__(self, "q_m", q_m)

    @staticmethod
    def _normalizar_vector(vector: tuple[float, ...], nombre: str) -> tuple[float, ...]:
        if len(vector) == 0:
            raise ValueError(f"{nombre} no puede estar vacio.")
        normalizado = tuple(float(valor) for valor in vector)
        if any(valor < 0 for valor in normalizado):
            raise ValueError(f"{nombre} no puede tener valores negativos.")
        return normalizado

    @property
    def q_e_total(self) -> float:
        "Retorna el volumen de equilibrio total."
        return float(sum(self.q_e))

    @property
    def q_r_total(self) -> float | None:
        "Retorna el volumen real total, o None si q_r no fue definido."
        if self.q_r is None:
            return None
        return float(sum(self.q_r))

    @property
    def q_m_total(self) -> float | None:
        "Retorna el volumen maximo total, o None si q_m no fue definido."
        if self.q_m is None:
            return None
        return float(sum(self.q_m))
