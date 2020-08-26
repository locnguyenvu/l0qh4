from dependency_injector import providers

from . import (
        core, 
        repository, 
        spending, 
        shared,
        users)

from .shared import (
        database)

config = providers.Configuration('config')
config.db.url.from_env('DATABASE_URL')

database = providers.Singleton(database.DB, url = config.db.url)

""" Factory """

spendinglog_repository_factory = providers.Factory(
       repository.SpendingLogRepository,
       db = database)

spendingcategory_repository_factory = providers.Factory(
       repository.SpendingCategoryRepository,
       db = database)

user_repository_factory = providers.Factory(
       repository.UserRepository,
       db = database)

""" Singleton """
from .repository.language_work_spending_category_map import LanguageWordSpendingCategoryMapRepository
languagewordspendingcategorymap_repository = providers.Singleton(
       LanguageWordSpendingCategoryMapRepository,
       db = database)

from .spending.categories import Categories as SpendingCategories
spendingcategories = providers.Singleton(
        SpendingCategories,
        spendingcategory_repository = spendingcategory_repository_factory)


users = providers.Singleton(
        users.Users,
        user_repository = user_repository_factory)

def factory(clsname: str):
    if clsname == 'spendinglog_repository':
        return spendinglog_repository_factory()
    if clsname == 'spendingcategory_repository':
        return spendingcategory_repository_factory()
    return None

def get(servicename: str):
    if servicename == 'db':
        return database()
    if servicename == 'languagewordspendingcategorymap_repository':
        return languagewordspendingcategorymap_repository()
    if servicename == 'spendingcategories':
        return spendingcategories()
    if servicename == 'users':
        return users()
    return None
