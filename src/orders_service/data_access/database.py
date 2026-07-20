from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE_FILE = PROJECT_ROOT / "labs" / "08_data_access_orm" / "orders.db"

DATABASE_URL = URL.create(
    drivername="sqlite+pysqlite",
    database=str(DATABASE_FILE),
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)
