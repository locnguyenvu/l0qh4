from sqlalchemy import and_, Boolean, Column, DateTime, Integer, String
from ...shared.orm_model import OrmModel

class SpendingCategory(OrmModel):

    __tablename__ = 'spending_category'

    id = Column(
            Integer(),
            primary_key = True)

    name = Column(
            String(),
            nullable = False)

    display_name = Column(
            String(),
            nullable = False)

    created_at = Column(
            DateTime,
            nullable = True)

    updated_at = Column(
            DateTime,
            nullable = False)

    def __repr__(self):
        return f"<(id={self.id}, name={self.name})>"

