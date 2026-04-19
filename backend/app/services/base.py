from sqlalchemy.orm import Session
from typing import Any


class BaseService:
    def __init__(self, session: Session):
        self.session = session

    def add_and_refresh(self, obj: Any) -> Any:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get(self, model: Any, id: Any) -> Any:
        return self.session.get(model, id)