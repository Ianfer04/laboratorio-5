from datetime import datetime
from typing import List, Dict
import logging

# Configuración del logging
logging.basicConfig(
    filename='log_contable.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MontoInvalidoError(Exception):
    """Excepción personalizada para montos inválidos."""
    pass

class LibroDiario:
    """Gestión contable básica de ingresos y egresos."""

    def __init__(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción al libro diario con validación y logging."""

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
            logging.info(f"Transacción registrada exitosamente: {transaccion}")

        except ValueError as ve:
            logging.error(f"Error de valor: {ve}", exc_info=True)
        except MontoInvalidoError as me:
            logging.error(f"Monto inválido: {me}", exc_info=True)
        except Exception as e:
            logging.error(f"Error inesperado al agregar transacción: {e}", exc_info=True)

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen
