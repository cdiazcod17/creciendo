from sqlalchemy.orm import Session
from typing import Any


class BaseService:
    
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, model_cls, identifier: str | int) -> Any | None:

        return self.session.get(model_cls, identifier)
    
    def add_and_refresh(self, obj: Any) -> Any:

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    
    def commit(self):

        self.session.commit()