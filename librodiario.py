from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(
    filename='log_contable.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MontoInvalidoError(Exception):
    pass

class LibroDiario:
    """Gestión contable básica de ingresos y egresos con manejo de errores."""

    def __init__(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        try:
            if tipo.lower() not in ("ingreso", "egreso"):
                raise ValueError("Tipo de transacción inválido. Use 'ingreso' o 'egreso'.")

            if monto <= 0:
                raise MontoInvalidoError("El monto debe ser mayor a cero.")

            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")

            transaccion = {
                "fecha": fecha_obj,
                "descripcion": descripcion,
                "monto": monto,
                "tipo": tipo.lower()
            }
            self.transacciones.append(transaccion)
            logging.info(f"Transacción registrada: {descripcion} - {monto} ({tipo})")

        except ValueError as ve:
            logging.error(f"Error de valor: {ve}")
        except MontoInvalidoError as me:
            logging.error(f"Monto inválido: {me}")
        except Exception as e:
            logging.error(f"Error inesperado: {e}")

    def calcular_resumen(self) -> Dict[str, float]:
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen

    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    try:
                        fecha, descripcion, monto, tipo = linea.strip().split(';')
                        self.agregar_transaccion(
                            datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y"),
                            descripcion,
                            float(monto),
                            tipo
                        )
                    except Exception as e:
                        logging.error(f"Error al procesar línea: {linea.strip()} | {e}")
        except FileNotFoundError:
            logging.error(f"Archivo no encontrado: {path}")

    def exportar_resumen(self, path: str) -> None:
        try:
            resumen = self.calcular_resumen()
            with open(path, 'w', encoding='utf-8') as archivo:
                archivo.write("Resumen contable:\n")
                archivo.write(f"Ingresos: {resumen['ingresos']:.2f}\n")
                archivo.write(f"Egresos: {resumen['egresos']:.2f}\n")
            logging.info("Resumen exportado correctamente.")
        except Exception as e:
            logging.error(f"Error al exportar resumen: {e}")
