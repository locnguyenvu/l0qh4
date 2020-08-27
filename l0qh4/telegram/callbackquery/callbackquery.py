from abc import ABCMeta, abstractmethod

class CallbackQuery(metaclass=ABCMeta):

    def __init__(self, update, context):
        self.update = update
        self.context = context
        self._onconstruct()

    def _onconstruct(self):
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass
