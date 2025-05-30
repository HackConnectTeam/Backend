from typing import List, Optional, TypeVar, Generic, Union
from sqlmodel import Session, SQLModel, select


ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Union[int, str]) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_all(
        self, db: Session, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.exec(select(self.model).offset(offset).limit(limit)).all()

    def get_by_field(
        self,
        db: Session,
        field_name: str,
        value: str,
        offset: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        return db.exec(
            select(self.model)
            .where(getattr(self.model, field_name) == value)
            .offset(offset)
            .limit(limit)
        ).all()

    def create(self, db: Session, *, obj_in: SQLModel) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: Union[ModelType, dict]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
