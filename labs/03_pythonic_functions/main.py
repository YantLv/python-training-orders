import time
from contextlib import contextmanager


def calculate_average(*values):
    """Calcula el promedio de una cantidad variable de valores."""

    if len(values) == 0:
        return 0

    total = sum(values)
    return total / len(values)


def show_details(**details):
    """Muestra una cantidad variable de datos nombrados."""

    for key, value in details.items():
        print(f"{key}: {value}")


def generate_batches(items, batch_size):
    """Divide una colección en lotes del tamaño indicado."""

    if batch_size <= 0:
        raise ValueError("El tamaño del lote debe ser mayor que cero.")

    for start in range(0, len(items), batch_size):
        end = start + batch_size
        yield items[start:end]


@contextmanager
def execution_timer(operation_name):
    """Mide el tiempo utilizado por un bloque de código."""

    start_time = time.perf_counter()

    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        print(f"La operación '{operation_name}'" f"tardó {elapsed_time:.4f} segundos.")


def retry(max_attempts=3, initial_delay=1):
    """Crea un decorador que reintenta una función cuando falla."""

    def decorator(function):
        def wrapper(*args, **kwargs):
            attempt = 1
            delay = initial_delay

            while attempt <= max_attempts:
                try:
                    return function(*args, **kwargs)

                except ValueError as error:
                    if attempt == max_attempts:
                        print("Se agotaron los intentos disponibles.")
                        raise error

                    print(
                        f"Intento {attempt} fallido: {error}. "
                        f"Nuevo intento en {delay} segundos."
                    )

                    time.sleep(delay)

                    attempt += 1
                    delay *= 2

        return wrapper

    return decorator


def main():
    """Ejecuta los ejemplos del laboratorio."""

    print("1. Ejemplo de *args")
    average = calculate_average(10, 20, 30, 40)
    print(f"Promedio: {average:.2f}")

    print()
    print("2. Ejemplo de **kwarg")
    show_details(
        customer="Ana",
        status="completed",
        total=850,
    )

    print()
    print("3. Conpresión de lista")
    numbers = [1, 2, 3, 4, 5, 6]
    even_squares = [number**2 for number in numbers if number % 2 == 0]

    print(f"Cuadrados de números pares: {even_squares}")

    print()
    print("4. Función lambda")
    orders = [
        {"order_code": "ORD-1001", "total": 850},
        {"order_code": "ORD-1002", "total": 320},
        {"order_code": "ORD-1003", "total": 1250},
    ]

    sorted_orders = sorted(
        orders,
        key=lambda order: order["total"],
        reverse=True,
    )

    print("Órdenes ordenadas por total:")

    for order in sorted_orders:
        print(f"{order['order_code']}: ${order['total']}")

    print()
    print("5. Generador por lotes")

    order_codes = [
        "ORD-1001",
        "ORD-1002",
        "ORD-1003",
        "ORD-1004",
        "ORD-1005",
        "ORD-1006",
        "ORD-1007",
    ]

    with execution_timer("Procesamiento por lotes "):
        for batch_number, batch in enumerate(
            generate_batches(order_codes, batch_size=3), start=1
        ):
            print(f"Lote {batch_number}: {batch}")
            time.sleep(0.2)

    print()
    print("6. Decorador de reintentos")

    pending_results = [False, False, True]

    @retry(max_attempts=3, initial_delay=0.5)
    def process_order(order_code):
        """Simula una operación que falla temporalmente."""

        result = pending_results.pop(0)

        if not result:
            raise ValueError(f"No fue posible procesar {order_code}")

        return f"La orden {order_code} fue procesada correctamente."

    message = process_order("ORD-1001")
    print(message)


if __name__ == "__main__":
    main()
