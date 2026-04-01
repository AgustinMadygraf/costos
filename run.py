"""
Path: run.py
"""


from src.infrastructure.numpy.app import calcular_punto_equilibrio
from src.interface_adapters.presenters import imprimir_resultados
from src.infrastructure.settings.config import ESCENARIO_BASE
from src.interface_adapters.controllers import PuntoEquilibrioController
from src.use_cases import CalcularPuntoEquilibrioUseCase


use_case = CalcularPuntoEquilibrioUseCase(calculator=calcular_punto_equilibrio)
controller = PuntoEquilibrioController(use_case=use_case)

resultado = controller.handle(
    cf=ESCENARIO_BASE.cf,
    productos=list(ESCENARIO_BASE.productos),
    pv=ESCENARIO_BASE.pv,
    cv=ESCENARIO_BASE.cv,
    m=ESCENARIO_BASE.m,
)

imprimir_resultados(resultado)
