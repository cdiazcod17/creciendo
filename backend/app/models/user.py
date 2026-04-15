from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.base import TimestampedUUIDModel
from app.core.enums import Roles

class User(TimestampedUUIDModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(
        String(250),
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    role: Mapped[Roles] = mapped_column(
        SQLEnum(Roles, name="roles"),
        default=Roles.user,
        nullable=False,
    )
    
    token_version: Mapped[int] = mapped_column(
        default=0, 
        nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    babies: Mapped[list["Baby"]] = relationship(
    "Baby",
    back_populates="user",
    cascade="all, delete-orphan"
)