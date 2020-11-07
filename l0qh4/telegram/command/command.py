import l0qh4
import telegram
import re

from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):

    def __call__(self, update, context):
        self.update = update
        self.context = context
        if not self.is_authorized():
            return
        self.process()

    @abstractmethod
    def process(self):
        pass

    @property
    def bot(self):
        return self.context.bot

    @property
    def effective_chat_id(self):
        return self.update.effective_chat.id

    @property
    def username(self):
        tlg_username = None
        if self.update.message is not None:
            tlg_username = self.update.message.from_user.username
        elif self.update.edited_message is not None:
            tlg_username = self.update.edited_message.from_user.username
        return tlg_username

    @property
    def message_id(self):
        return self.update.message.message_id

    def is_authorized(self) -> bool:
        tlg_username = self.username
        if tlg_username is None:
            return False
        users = l0qh4.get('users')
        return users.is_active(telegram_username = tlg_username)


    def reply(self, text: str, parse_mode = None):
        self.bot.send_message(
                chat_id = self.effective_chat_id,
                text = text,
                parse_mode = parse_mode)

    def get_messagecontent(self):
        return self.update.message.text

    def hasOption(self, optionAlias) -> bool:
        message_chunks = self.update.message.text.split(' ')
        for charecters in message_chunks:
            if not re.match(r'^\-{1,2}[a-zA-Z]+', charecters):
                continue

            return re.sub(r'^\-{1,2}', '', charecters) == optionAlias

