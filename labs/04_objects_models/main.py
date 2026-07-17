from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

OrderStatus = Literal["pending", "completed", "cancelled"]


@dataclass
class OrderItem:
    """Representa un artículo incluido en una orden."""

    product_name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del artículo."""

        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    """Representa una orden con sus artículos y cálculos."""

    order_code: str
    customer: str
    items: list[OrderItem]
    discount: float = 0.0
    status: OrderStatus = "pending"

    def __post_init__(self) -> None:
        """Valida los datos básicos después de crear la orden."""

        if len(self.items) == 0:
            raise ValueError("La orden debe contener al menos un artículo.")

        if self.discount < 0 or self.discount > 1:
            raise ValueError("El descuento debe estar entre 0 y 1.")

    @property
    def subtotal(self) -> float:
        """Calcula la suma de los artículos antes del descuento."""

        total: float = 0.0

        for item in self.items:
            total += item.subtotal

        return round(total, 2)

    @property
    def total(self) -> float:
        """Calcula el total después de aplicar el descuento."""

        discounted_total = self.subtotal * (1 - self.discount)
        return round(discounted_total, 2)

    def __lt__(self, other: object) -> bool:
        """Compara dos órdenes utilizando su total."""

        if not isinstance(other, Order):
            return NotImplemented

        return self.total < other.total


class OrderItemIn(BaseModel):
    """Valida un artículo recibido como entrada."""

    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class OrderIn(BaseModel):
    """Valida los datos recibidos para crear una orden."""

    order_code: str = Field(pattern=r"^ORD-\d{4}$")
    customer: str = Field(min_length=1)
    items: list[OrderItemIn] = Field(min_length=1)
    discount: float = Field(default=0.0, ge=0, le=1)
    status: OrderStatus = "pending"


class OrderOut(BaseModel):
    """Representa la información que se mostrará de una orden."""

    order_code: str
    customer: str
    status: OrderStatus
    subtotal: float
    discount: float
    total: float


def convert_to_entity(order_input: OrderIn) -> Order:
    """Convierte un modelo de entrada en una entidad Order."""

    items: list[OrderItem] = []

    for item_input in order_input.items:
        item = OrderItem(
            product_name=item_input.product_name,
            quantity=item_input.quantity,
            unit_price=item_input.unit_price,
        )

        items.append(item)

    return Order(
        order_code=order_input.order_code,
        customer=order_input.customer,
        items=items,
        discount=order_input.discount,
        status=order_input.status,
    )


def convert_to_output(order: Order) -> OrderOut:
    """Convierte una entidad Order en un modelo de salida."""

    return OrderOut(
        order_code=order.order_code,
        customer=order.customer,
        status=order.status,
        subtotal=order.subtotal,
        discount=order.discount,
        total=order.total,
    )


def main() -> None:
    """Ejecuta las demostraciones del laboratorio."""

    first_data = {
        "order_code": "ORD-2001",
        "customer": "Ana",
        "items": [
            {
                "product_name": "Keyboard",
                "quantity": 2,
                "unit_price": 450,
            },
            {
                "product_name": "Mouse",
                "quantity": 1,
                "unit_price": 300,
            },
        ],
        "discount": 0.10,
        "status": "completed",
    }

    second_data = {
        "order_code": "ORD-2002",
        "customer": "Luis",
        "items": [
            {
                "product_name": "Monitor",
                "quantity": 1,
                "unit_price": 2400,
            },
        ],
        "discount": 0.05,
    }

    try:
        first_input = OrderIn.model_validate(first_data)
        second_input = OrderIn.model_validate(second_data)

        first_order = convert_to_entity(first_input)
        second_order = convert_to_entity(second_input)

        first_output = convert_to_output(first_order)
        second_output = convert_to_output(second_order)

        print("Primera orden:")
        print(first_output.model_dump())

        print()
        print("Segunda orden:")
        print(second_output.model_dump())

        print()
        print("Comparación:")
        print(
            f"¿La primera orden cuesta menos que la segunda? "
            f"{first_order < second_order}"
        )

    except ValidationError as error:
        print("Los datos de entrada no son válidos:")
        print(error)

    print()
    print("Validación de datos incorrectos:")

    invalid_data = {
        "order_code": "2003",
        "customer": "Carla",
        "items": [
            {
                "product_name": "Webcam",
                "quantity": 0,
                "unit_price": 700,
            },
        ],
        "discount": 1.50,
    }

    try:
        OrderIn.model_validate(invalid_data)

    except ValidationError as error:
        print("Pydantic rechazó correctamente los datos:")
        print(error)


if __name__ == "__main__":
    main()
