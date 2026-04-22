from typing import Any, Generic, Type, TypeVar
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id: UUID) -> T | None:
        return self.session.get(self.model, id)

    def list(self) -> list[T]:
        return list(self.session.execute(select(self.model)).scalars().all())

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()

    def update(self) -> None:
        self.session.commit()
