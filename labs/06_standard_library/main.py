import csv
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

CSV_FILE = DATA_DIR / "orders.csv"
CONFIG_FILE = BASE_DIR / "config.yaml"
LOG_FILE = LOG_DIR / "laboratory.log"


def configure_logging():
    """Configura los mensajes de registro en consola y archivo."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def load_config():
    """Carga las opciones contenidas en el archivo YAML."""
    with CONFIG_FILE.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


def load_orders():
    """Carga y convierte las órdenes contenidas en el CSV."""

    orders = []

    with CSV_FILE.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            order = {
                "order_code": row["order_code"],
                "customer": row["customer"],
                "status": row["status"],
                "total": float(row["total"]),
                "created_at": row["created_at"],
            }

            orders.append(order)

    logging.info("Se cargaron %s órdenes desde el CSV.", len(orders))

    return orders


def filter_orders(orders, selected_status, minimum_total):
    """Filtra órdenes por estado y monto mínimo."""

    filtered_orders = []

    for order in orders:
        if order["status"] == selected_status and order["total"] >= minimum_total:
            filtered_orders.append(order)

    if len(filtered_orders) == 0:
        logging.warning("Ninguna orden cumplió los filtros establecidos.")
    else:
        logging.info(
            "%s órdenes cumplieron los filtros.",
            len(filtered_orders),
        )

    return filtered_orders


def calculate_metrics(orders):
    """Calcula métricas generales de las órdenes filtradas."""

    order_count = len(orders)
    total_amount = 0.0

    for order in orders:
        total_amount += order["total"]

    if order_count > 0:
        average_amount = total_amount / order_count
    else:
        average_amount = 0.0

    return {
        "order_count": order_count,
        "total_amount": round(total_amount, 2),
        "average_amount": round(average_amount, 2),
    }


def get_report_datetime(timezone_name):
    """Obtiene la fecha actual en la zona horaria indicada."""

    timezone = ZoneInfo(timezone_name)
    current_datetime = datetime.now(timezone)

    return current_datetime.isoformat()


def get_python_version():
    """Obtiene la versión de Python mediante subprocess."""

    result = subprocess.run(
        [sys.executable, "--version"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def save_report(report, output_name):
    """Guarda el reporte en formato JSON."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / output_name

    with output_file.open(mode="w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info("El reporte fue guardado en %s.", output_file)

    return output_file


def main():
    """Coordina la ejecución del laboratorio."""

    configure_logging()

    logging.info("Inicio del procesamiento.")

    try:
        config = load_config()
        orders = load_orders()

        selected_status = config["selected_status"]
        minimum_total = config["minimum_total"]
        timezone_name = config["timezone"]
        output_name = config["output_file"]

        filtered_orders = filter_orders(
            orders,
            selected_status,
            minimum_total,
        )

        metrics = calculate_metrics(filtered_orders)

        report = {
            "generated_at": get_report_datetime(timezone_name),
            "python_version": get_python_version(),
            "filters": {
                "status": selected_status,
                "minimum_total": minimum_total,
            },
            "metrics": metrics,
            "orders": filtered_orders,
        }

        output_file = save_report(report, output_name)

        print()
        print("Procesamiento completado.")
        print(f"Órdenes procesadas: {metrics['order_count']}")
        print(f"Monto total: ${metrics['total_amount']:.2f}")
        print(f"Monto promedio: ${metrics['average_amount']:.2f}")
        print(f"Reporte generado: {output_file}")

        logging.info("Procesamiento finalizado correctamente.")

    except FileNotFoundError as error:
        logging.error("No se encontró un archivo requerido: %s", error)

    except KeyError as error:
        logging.error("Falta una opción o columna obligatoria: %s", error)

    except ValueError as error:
        logging.error("Se encontró un valor inválido: %s", error)

    except subprocess.CalledProcessError as error:
        logging.error("No fue posible ejecutar el subproceso: %s", error)


if __name__ == "__main__":
    main()
