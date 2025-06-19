from librodiario import LibroDiario

libro = LibroDiario()

# Transacciones corregidas
libro.agregar_transaccion('18/06/2025', 'Compra de laptop', 780, 'egreso')
libro.agregar_transaccion('18/06/2025', 'Venta de sensor TK-110', 780, 'ingreso')  # corregido: 'Ingreso' → 'ingreso'
libro.agregar_transaccion('18/06/2025', 'Compra de insumos de oficina', -85.60, 'egreso')  # se activará la excepción

print(libro.calcular_resumen())
