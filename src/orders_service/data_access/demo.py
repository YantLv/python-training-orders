from decimal import Decimal

from orders_service.data_access.crud import (
    OrderItemInput,
    create_order,
    create_user,
    delete_order,
    get_order_by_id,
    get_user_by_email,
    list_orders,
    update_order_status,
)
from orders_service.data_access.database import SessionLocal

DEMO_EMAIL = "ana@example.com"


def main() -> None:
    """Ejecuta una demostración del CRUD."""

    with SessionLocal() as session:
        user = get_user_by_email(
            session,
            DEMO_EMAIL,
        )

        if user is None:
            user = create_user(
                session,
                name="Ana",
                email=DEMO_EMAIL,
            )

            print(f"Usuario creado: {user}")
        else:
            print(f"Usuario existente: {user}")

        order = create_order(
            session,
            user_id=user.id,
            items=[
                OrderItemInput(
                    product_name="Keyboard",
                    quantity=2,
                    unit_price=Decimal("450.00"),
                ),
                OrderItemInput(
                    product_name="Mouse",
                    quantity=1,
                    unit_price=Decimal("300.00"),
                ),
            ],
        )

        print()
        print(f"Orden creada: {order}")
        print(f"Total inicial: ${order.total:.2f}")

        stored_order = get_order_by_id(
            session,
            order.id,
        )

        if stored_order is not None:
            print()
            print("Orden consultada:")
            print(f"Identificador: {stored_order.id}")
            print(f"Estado: {stored_order.status}")
            print(f"Artículos: {len(stored_order.items)}")
            print(f"Total: ${stored_order.total:.2f}")

        updated_order = update_order_status(
            session,
            order.id,
            "completed",
        )

        if updated_order is not None:
            print()
            print("Estado actualizado: " f"{updated_order.status}")

        orders = list_orders(session)

        print()
        print(f"Órdenes registradas: {len(orders)}")

        for stored_order in orders:
            print(
                f"- Orden {stored_order.id}: "
                f"${stored_order.total:.2f} "
                f"({stored_order.status})"
            )

        was_deleted = delete_order(
            session,
            order.id,
        )

        print()
        print(f"Orden eliminada: {was_deleted}")
        print("Órdenes restantes: " f"{len(list_orders(session))}")


if __name__ == "__main__":
    main()
