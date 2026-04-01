"""
Path: src/entities/costo_fijo.py
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class CostoFijo:
    """
    Representa costos fijos totales para un periodo de analisis.
    """

    monto: Decimal
    periodo: str = "mensual"
    moneda: str = "ARS"

    def __post_init__(self) -> None:
        monto = Decimal(str(self.monto)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if monto < 0:
            raise ValueError("El costo fijo no puede ser negativo.")
        if not self.periodo.strip():
            raise ValueError("El periodo de costo fijo no puede estar vacio.")
        if not self.moneda.strip():
            raise ValueError("La moneda de costo fijo no puede estar vacia.")
        object.__setattr__(self, "monto", monto)
