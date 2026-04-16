from sqlalchemy.orm import Session
from typing import Any


class BaseService:
    def __init__(self, session: Session):
        self.session = session