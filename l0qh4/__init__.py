from dotenv import load_dotenv
load_dotenv()

import os
from dependency_injector import containers, providers


APP_PATH=os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(APP_PATH)
RESOURCE_PATH = os.path.join(BASE_PATH, 'var', 'resources')

app_container = containers.DynamicContainer()
app_container.config = providers.Configuration('config')

app_container.config.db.url.from_env('DATABASE_URL')
app_container.config.email.account.from_env('EMAIL_ACCOUNT')

""" Singleton """
from .shared import database
app_container.database = providers.Singleton(database.DB, url = app_container.config.db.url)

from .repository.spendingcategory_repository import SpendingCategoryRepository
app_container.spendingcategory_repository = providers.Singleton(
        SpendingCategoryRepository,
        database = app_container.database)
from .spending.categories import Categories
app_container.spendingcategories = providers.Singleton(
        Categories,
        sc_repository = app_container.spendingcategory_repository)

from .repository.user_repository import UserRepository
app_container.user_repository = providers.Singleton(
        UserRepository,
        database = app_container.database)
from .user.users import Users
app_container.users = providers.Singleton(
        Users,
        user_repository = app_container.user_repository)

from .repository.config_repository import ConfigRepository
config_repository = providers.Singleton(
        ConfigRepository,
        database = app_container.database)

def factory(clsname: str):
    return None

def get(servicename: str):
    if servicename == 'db':
        return app_container.database()
    if servicename == 'spendingcategories':
        return app_container.spendingcategories()
    if servicename == 'users':
        return app_container.users()
    return None

""" Load config from DB """ 
for dbconfig in config_repository().find_all():
    app_container.config.set(dbconfig.path, dbconfig.value)

def get_config(path: str):
    return app_container.config.get(path)
