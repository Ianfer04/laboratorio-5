from datetime import datetime
from typing import List, Dict
import logging

# Configurar logging
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

    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        """Carga transacciones desde un archivo CSV con validaciones."""
        try:
            with open(path, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    try:
                        partes = linea.strip().split(';')
                        if len(partes) != 4:
                            raise ValueError("La línea no tiene 4 campos esperados.")

                        fecha_iso, descripcion, monto_str, tipo = partes
                        fecha_formateada = datetime.strptime(fecha_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
                        monto = float(monto_str)

                        self.agregar_transaccion(fecha_formateada, descripcion, monto, tipo.strip().lower())

                    except Exception as e:
                        logging.error(f"Error al procesar línea: {linea.strip()} - {e}", exc_info=True)

        except FileNotFoundError:
            logging.error(f"Archivo no encontrado: {path}", exc_info=True)
        except Exception as e:
            logging.error(f"Error al leer el archivo: {e}", exc_info=True)

    
    
