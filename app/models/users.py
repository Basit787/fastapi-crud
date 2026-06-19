from sqlalchemy import Enum as SAEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.config.database import Base
from app.models.roles import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    hashed_password: Mapped[str] = mapped_column(String(255))

    role: Mapped[Role] = mapped_column(
        SAEnum(Role, native_enum=False, length=20),
        default=Role.USER,
    )
