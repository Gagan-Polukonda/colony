from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Forager(Base):
    __tablename__ = "foragers"
    __table_args__ = {"schema": "users"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    api_key: Mapped[str] = mapped_column(unique=True)