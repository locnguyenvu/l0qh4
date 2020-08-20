from .repository import UserRepository

class Users:

    def __init__(self, user_repository: UserRepository) -> None:
        self.__data = user_repository.listall()

    def find_user(self, **kwargs):
        for key, value in kwargs.items():
            mateched = [user for user in self.__data if getattr(user, key, None) == value]
            break
        if len(mateched) == 0:
            return None
        else:
            return mateched[0]

    def get_alias(self, **kwargs):
        user = self.find_user(**kwargs)
        if user is not None:
            return user.alias
        return None

    def is_active(self, **kwargs):
        user = self.find_user(**kwargs)
        if user is not None:
            return user.is_active
        return None

