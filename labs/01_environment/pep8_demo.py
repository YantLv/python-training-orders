def calculate_total(prices: list[float]) -> float:
    """Calculate the sum of a collection of prices."""
    return sum(prices)


if __name__ == "__main__":
    examples_prices = [10.0, 20.0, 30.0]
    print(calculate_total(examples_prices))
