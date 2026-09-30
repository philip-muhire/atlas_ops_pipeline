from sqlalchemy.orm import Session

class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, model, skip: int, limit: int):
        total = self.db.query(model).count()
        items = self.db.query(model).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, model, field_name: str, item_id: str):
        return self.db.query(model).filter(getattr(model, field_name) == item_id).first()

    def create(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
