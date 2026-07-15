import json
import re


def load_orders(file_path):
    """Carga las órdenes desde un archivo JSON."""

    with open(file_path, encoding="utf-8") as file:
        orders = json.load(file)

    if not isinstance(orders, list):
        raise ValueError("El contenido principal del JSON debe ser una lista.")

    return orders


def filter_orders(orders, status, minimum_total):
    """Filtra órdenes por estado y monto mínimo."""

    return [
        order
        for order in orders
        if order["status"] == status and order["total"] >= minimum_total
    ]


def calculate_summary(orders):
    """Calcula el número, total y promedio de las órdenes recibidas."""

    order_count = len(orders)
    total_amount = 0

    for order in orders:
        total_amount += order["total"]

    if order_count > 0:
        average_amount = total_amount / order_count
    else:
        average_amount = 0

    summary = {
        "order_count": order_count,
        "total_amount": round(total_amount, 2),
        "average_amount": round(average_amount, 2),
    }

    return summary


def get_status_message(status):
    """Devuelve una descripción en español para cada estado."""

    match status:
        case "completed":
            return "completada"
        case "pending":
            return "pendiente"
        case "cancelled":
            return "cancelada"
        case _:
            return "desconocida"


def is_valid_order_code(order_code):
    """Compruena si el código tiene el formato ORD-0000."""

    pattern = r"^ORD-\d{4}$"
    return re.fullmatch(pattern, order_code) is not None


def print_orders(orders):
    """Muestra las órdenes procesadas."""

    for order in orders:
        order_code = order["order_code"]
        status_message = get_status_message(order["status"])

        if is_valid_order_code(order_code):
            code_message = "código válido"
        else:
            code_message = "código inválido"

        print(
            f"{order_code} | "
            f"{order['customer']} | "
            f"{status_message} | "
            f"${order['total']:.2f} | "
            f"{code_message}"
        )


def main():
    """Coordina la ejecución completa del laboratorio."""

    file_name = input("Escribe el nombre del archivo JSON [orders.json]: ").strip()

    if file_name == "":
        file_name = "orders.json"

    file_path = f"labs/02_fundamentals/data/{file_name}"

    selected_status = "completed"
    minimum_total = 500

    try:
        orders = load_orders(file_path)

        filtered_orders = filter_orders(
            orders,
            selected_status,
            minimum_total,
        )

        summary = calculate_summary(filtered_orders)

        print()
        print("Órdenes filtradas:")
        print_orders(filtered_orders)

        print()
        print("Resumen:")
        print(f"Número de órdenes: {summary['order_count']}")
        print(f"Monto total: ${summary['total_amount']:.2f}")
        print(f"Monto promedio: ${summary['average_amount']:.2f}")

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{file_name}'.")

    except json.JSONDecodeError:
        print(f"Error: el archivo '{file_name}' no contiene un JSON válido.")

    except KeyError as error:
        print(f"Error: falta el campo obligatorio {error}.")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
