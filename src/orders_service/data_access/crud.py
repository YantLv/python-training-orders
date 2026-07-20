from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from orders_service.data_access.models import (
    Order,
    OrderItem,
    User,
)

OrderStatus = Literal[
    "pending",
    "completed",
    "cancelled",
]


@dataclass(frozen=True)
class OrderItemInput:
    """Representa los datos necesarios para crear un artículo."""

    product_name: str
    quantity: int
    unit_price: Decimal


def create_user(
    session: Session,
    name: str,
    email: str,
) -> User:
    """Crea y guarda un usuario."""

    existing_user = get_user_by_email(session, email)

    if existing_user is not None:
        raise ValueError(f"Ya existe un usuario con el correo {email}.")

    user = User(
        name=name,
        email=email,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_email(
    session: Session,
    email: str,
) -> User | None:
    """Busca un usuario mediante su correo electrónico."""

    statement = select(User).where(User.email == email)

    return session.scalar(statement)


def create_order(
    session: Session,
    user_id: int,
    items: list[OrderItemInput],
) -> Order:
    """Crea una orden con sus artículos."""

    user = session.get(User, user_id)

    if user is None:
        raise ValueError(f"No existe un usuario con identificador {user_id}.")

    if len(items) == 0:
        raise ValueError("La orden debe contener al menos un artículo.")

    order_items: list[OrderItem] = []

    for item_input in items:
        if item_input.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if item_input.unit_price < 0:
            raise ValueError("El precio no puede ser negativo.")

        order_item = OrderItem(
            product_name=item_input.product_name,
            quantity=item_input.quantity,
            unit_price=item_input.unit_price,
        )

        order_items.append(order_item)

    order = Order(
        user=user,
        items=order_items,
        status="pending",
    )

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


def get_order_by_id(
    session: Session,
    order_id: int,
) -> Order | None:
    """Busca una orden y carga sus artículos."""

    statement = (
        select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    )

    return session.scalar(statement)


def list_orders(session: Session) -> list[Order]:
    """Devuelve todas las órdenes registradas."""

    statement = select(Order).options(selectinload(Order.items)).order_by(Order.id)

    return list(session.scalars(statement))


def update_order_status(
    session: Session,
    order_id: int,
    status: OrderStatus,
) -> Order | None:
    """Actualiza el estado de una orden."""

    order = session.get(Order, order_id)

    if order is None:
        return None

    order.status = status

    session.commit()
    session.refresh(order)

    return order


def delete_order(
    session: Session,
    order_id: int,
) -> bool:
    """Elimina una orden mediante su identificador."""

    order = session.get(Order, order_id)

    if order is None:
        return False

    session.delete(order)
    session.commit()

    return True
