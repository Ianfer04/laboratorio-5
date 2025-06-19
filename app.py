from librodiario import LibroDiario

def main():
    libro = LibroDiario()

    print("Cargando transacciones desde archivo CSV...\n")
    libro.cargar_transacciones_desde_archivo("trans.csv")

    print("Transacciones registradas:\n")
    for t in libro.transacciones:
        fecha_str = t["fecha"].strftime("%d/%m/%Y")
        print(f"- {fecha_str} | {t['descripcion']} | ${t['monto']:.2f} | {t['tipo']}")

    print("\nResumen contable:\n")
    resumen = libro.calcular_resumen()
    print(f"Total ingresos: ${resumen['ingresos']:.2f}")
    print(f"Total egresos: ${resumen['egresos']:.2f}\n")

    print("Exportando resumen a archivo 'resumen.txt'...\n")
    libro.exportar_resumen("resumen.txt")

    print("Proceso completado. Revisa 'log_contable.log' y 'resumen.txt' para más detalles.\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        from datetime import datetime
        import logging
        logging.basicConfig(filename='log_contable.log', level=logging.ERROR)
        logging.error(f"Error no controlado en la app: {e}")
        print("Ocurrió un error inesperado. Revisa 'log_contable.log' para más detalles.")
