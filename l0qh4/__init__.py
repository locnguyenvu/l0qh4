from dependency_injector import providers

from . import (
        core, 
        repository, 
        spending, 
        shared)

from .shared import (
        database)

config = providers.Configuration('config')
config.db.url.from_env('DATABASE_URL')
database = providers.Singleton(database.DB, url = config.db.url)

""" Singleton """
from .repository.spendingcategory_repository import SpendingCategoryRepository
spendingcategory_repository = providers.Singleton(
        SpendingCategoryRepository,
        database = database)
from .spending.categories import Categories
spendingcategories = providers.Singleton(
        Categories,
        sc_repository = spendingcategory_repository)

from .repository.user_repository import UserRepository
user_repository = providers.Singleton(
        UserRepository,
        database = database)
from .user.users import Users
users = providers.Singleton(
        Users,
        user_repository = user_repository)

def factory(clsname: str):
    return None

def get(servicename: str):
    if servicename == 'db':
        return database()
    if servicename == 'spendingcategories':
        return spendingcategories()
    if servicename == 'users':
        return users()
    return None
