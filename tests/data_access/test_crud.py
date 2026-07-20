from decimal import Decimal

from sqlalchemy.orm import Session

from orders_service.data_access.crud import (
    OrderItemInput,
    create_order,
    create_user,
    delete_order,
    get_order_by_id,
    get_user_by_email,
    update_order_status,
)


def test_create_and_read_user(
    session: Session,
) -> None:
    """Comprueba la creación y consulta de usuarios."""

    created_user = create_user(
        session,
        name="Ana",
        email="ana@example.com",
    )

    stored_user = get_user_by_email(
        session,
        "ana@example.com",
    )

    assert stored_user is not None
    assert stored_user.id == created_user.id
    assert stored_user.name == "Ana"
    assert stored_user.email == "ana@example.com"


def test_create_order_with_items(
    session: Session,
) -> None:
    """Comprueba la creación y cálculo de una orden."""

    user = create_user(
        session,
        name="Luis",
        email="luis@example.com",
    )

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

    stored_order = get_order_by_id(
        session,
        order.id,
    )

    assert stored_order is not None
    assert stored_order.user_id == user.id
    assert len(stored_order.items) == 2
    assert stored_order.total == Decimal("1200.00")
    assert stored_order.status == "pending"


def test_update_order_status(
    session: Session,
) -> None:
    """Comprueba la actualización de una orden."""

    user = create_user(
        session,
        name="Carla",
        email="carla@example.com",
    )

    order = create_order(
        session,
        user_id=user.id,
        items=[
            OrderItemInput(
                product_name="Monitor",
                quantity=1,
                unit_price=Decimal("2400.00"),
            ),
        ],
    )

    updated_order = update_order_status(
        session,
        order.id,
        "completed",
    )

    assert updated_order is not None
    assert updated_order.status == "completed"


def test_delete_order(
    session: Session,
) -> None:
    """Comprueba la eliminación de una orden."""

    user = create_user(
        session,
        name="Sofia",
        email="sofia@example.com",
    )

    order = create_order(
        session,
        user_id=user.id,
        items=[
            OrderItemInput(
                product_name="Webcam",
                quantity=1,
                unit_price=Decimal("700.00"),
            ),
        ],
    )

    was_deleted = delete_order(
        session,
        order.id,
    )

    stored_order = get_order_by_id(
        session,
        order.id,
    )

    assert was_deleted is True
    assert stored_order is None
