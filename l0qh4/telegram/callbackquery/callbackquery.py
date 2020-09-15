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

    @property
    def bot(self):
        return self.context.bot

    @property
    def effective_chat_id(self):
        return self.update.effective_chat.id

    def reply(self, text: str, parse_mode = None):
        self.bot.send_message(
                chat_id = self.effective_chat_id,
                text = text,
                parse_mode = parse_mode)
