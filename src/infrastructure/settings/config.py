"""
path: src/infrastructure/settings/config.py
"""

from decimal import Decimal

from src.entities.costo_fijo import CostoFijo


COSTO_FIJO_MENSUAL = CostoFijo(
    monto=Decimal("100000.00"),
    periodo="mensual",
    moneda="ARS",
)
