from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""

    pass


class User(Base):
    """Representa un usuario almacenado en la base de datos."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    orders: Mapped[list[Order]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Devuelve una representación legible del usuario."""

        return f"User(id={self.id!r}, " f"name={self.name!r}, " f"email={self.email!r})"


class Order(Base):
    """Representa una orden perteneciente a un usuario."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    user: Mapped[User] = relationship(
        back_populates="orders",
    )
    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    @property
    def total(self) -> Decimal:
        """Calcula el total de los artículos de la orden."""

        return sum(
            (item.subtotal for item in self.items),
            Decimal("0.00"),
        )

    def __repr__(self) -> str:
        """Devuelve una representación legible de la orden."""

        return (
            f"Order(id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"status={self.status!r})"
        )


class OrderItem(Base):
    """Representa un artículo perteneciente a una orden."""

    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_order_items_unit_price_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(150))
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        index=True,
    )

    order: Mapped[Order] = relationship(
        back_populates="items",
    )

    @property
    def subtotal(self) -> Decimal:
        """Calcula el subtotal del artículo."""

        return self.unit_price * self.quantity

    def __repr__(self) -> str:
        """Devuelve una representación legible del artículo."""

        return (
            f"OrderItem(id={self.id!r}, "
            f"product_name={self.product_name!r}, "
            f"quantity={self.quantity!r}, "
            f"unit_price={self.unit_price!r})"
        )
