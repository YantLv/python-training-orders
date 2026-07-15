def calculate_total(prices: list[float]) -> float:
    """Calcula la suma de una lista de precios."""
    return sum(prices)


if __name__ == "__main__":
    examples_prices = [10.0, 20.0, 30.0]
    print(calculate_total(examples_prices))
