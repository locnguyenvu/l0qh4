import l0qh4

from dependency_injector import containers, providers
from telegram.ext import Updater
from . import (
        core, 
        repository, 
        spending, 
        users)
from .telegram.handler import CallbackQueryHandler, CommandHandler, MessageHandler

class BotContainer(containers.DeclarativeContainer):

    config = l0qh4.config

    database = l0qh4.database

    spendinglog_repository = l0qh4.spendinglog_repository_factory

    user_repository = l0qh4.user_repository_factory

    users = l0qh4.users

    command_handler = providers.Factory(
            CommandHandler,
            users = users,
            spendingcategories = l0qh4.spendingcategories,
            spendinglog_repository = spendinglog_repository)

    message_handler = providers.Factory(
            MessageHandler,
            users = users,
            spendingcategories = l0qh4.spendingcategories,
            spendinglog_repository = spendinglog_repository)

    callbackquery_handler = providers.Factory(
            CallbackQueryHandler,
            users = users,
            spendingcategories = l0qh4.spendingcategories,
            spendinglog_repository = spendinglog_repository)

class ConsoleContainer(containers.DeclarativeContainer):

    config = l0qh4.config 

    database = l0qh4.database

