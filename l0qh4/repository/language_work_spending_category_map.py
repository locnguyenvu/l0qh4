from datetime import datetime
from sqlalchemy import and_, Boolean, Column, DateTime, Integer, String
from ..core import Base, BaseRepository

class LanguageWordSpendingCategoryMap(Base):

    __tablename__ = 'language_word_spending_category_map'

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

class LanguageWordSpendingCategoryMapRepository(BaseRepository):

    @classmethod
    def orm_class(cls):
        return LanguageWordSpendingCategoryMap

    def add(self, word: str, category_id: int, category_name: str, score: int):
        instance = self.orm_class()()
        instance.word = word
        instance.category_id = category_id
        instance.score = score
        instance.created_at = datetime.now()
        instance.updated_at = datetime.now()
        self._session.add(instance)
        self._session.commit()
