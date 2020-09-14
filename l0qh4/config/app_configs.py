from ..repository.config_repository import ConfigRepository

class AppConfigs(object):

    def __init__(self, config_repository: ConfigRepository):
        self._c_repository = config_repository
        self.__data = config_repository.find_all()

    def get_config(path: str):
        for config in self.__data:
            if config.path == path:
                return config.value
        return None
