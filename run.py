"""
Path: run.py
"""


from src.infrastructure.numpy.app import calcular_punto_equilibrio, imprimir_resultados




productos = ["Bolsa A", "Bolsa B", "Bolsa C"]

pv = [120, 150, 100]      # precios de venta unitarios
cv = [70, 90, 60]         # costos variables unitarios
m = [0.5, 0.3, 0.2]       # mix de ventas (debe sumar 1)
cf = 100000               # costos fijos totales

resultado = calcular_punto_equilibrio(
    cf=cf,
    productos=productos,
    pv=pv,
    cv=cv,
    m=m
)

imprimir_resultados(resultado)
