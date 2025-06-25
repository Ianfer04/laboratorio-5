from datetime import datetime
from typing import List, Dict

class MontoInvalidoError(Exception):
    """Excepción personalizada ."""
    pass

class LibroDiario:
    """Gestión contable básica de ingresos y egresos."""

    def _init_(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción al libro diario."""
        tipo = tipo.lower()
        if tipo not in ("ingreso", "egreso"):
            raise ValueError(f"Tipo de transacción inválido ({tipo}). Use 'ingreso' o 'egreso'.")
        
        try:
            obj_fecha= datetime.strptime(fecha, "%d/%m/%Y")
        except Exception as e:
            raise ValueError(f" Formato de fecha invalida({fecha}). use 'dd/mm/yyyy'.")

        if monto < 0:
            raise ValueError(f" monto invalido({monto}). el monto debe ser mayor a 0 .")


        transaccion = {
            "fecha": datetime.strptime(fecha, "%d/%m/%Y"),
            "descripcion": descripcion,
            "monto": monto,
            "tipo": tipo
        }
        self.transacciones.append(transaccion)

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen