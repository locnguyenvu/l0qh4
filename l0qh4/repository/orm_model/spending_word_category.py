from sqlalchemy import and_, Boolean, Column, DateTime, Integer, String
from ...shared.orm_model import OrmModel

class SpendingWordCategory(OrmModel):

    __tablename__ = 'spending_word_category'

    id = Column(
            Integer(),
            primary_key = True)

    word = Column(
            String(),
            nullable = False)

    category_id = Column(
            Integer(),
            nullable = False)

    category_name = Column(
            String(),
            nullable = True)

    score = Column(
            Integer(),
            nullable = False)

    created_at = Column(
            DateTime,
            nullable = True)

    updated_at = Column(
            DateTime,
            nullable = False)

