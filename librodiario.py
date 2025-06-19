from datetime import datetime
from typing import List, Dict

class MontoInvalidoError(Exception):
    """Excepción personalizada para montos inválidos."""
    pass

class LibroDiario:
    """Gestión contable básica de ingresos y egresos."""

    def __init__(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción al libro diario con validaciones."""

        try:
            if tipo not in ("ingreso", "egreso"):
                raise ValueError("Tipo de transacción inválido. Use 'ingreso' o 'egreso'.")

            if monto <= 0:
                raise MontoInvalidoError("El monto debe ser mayor que cero.")

            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")

            transaccion = {
                "fecha": fecha_dt,
                "descripcion": descripcion,
                "monto": monto,
                "tipo": tipo
            }

            self.transacciones.append(transaccion)

        except Exception as e:
            print(f"Error al agregar transacción: {e}")

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen
