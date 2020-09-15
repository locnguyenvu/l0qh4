import l0qh4

from dependency_injector import containers, providers

class BotContainer(containers.DeclarativeContainer):

    config = providers.Configuration('config')


class ConsoleContainer(containers.DeclarativeContainer):

    config = providers.Configuration('config')

