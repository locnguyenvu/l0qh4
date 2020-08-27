from ..shared.repository import Repository
from .orm_model.user import User

class UserRepository(Repository):

    ormclass = User

    domainclass = None
