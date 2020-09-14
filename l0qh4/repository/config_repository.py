from .orm_model.config import Config
from ..shared.repository import Repository

class ConfigRepository(Repository):

    ormclass = Config

    domainclass = None
