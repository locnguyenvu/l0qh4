import l0qh4

from dependency_injector import containers, providers
from telegram.ext import Updater
from . import (
        core, 
        repository, 
        spending)

class BotContainer(containers.DeclarativeContainer):

    config = l0qh4.config


class ConsoleContainer(containers.DeclarativeContainer):

    config = l0qh4.config 

    database = l0qh4.database

