from l0qh4.spending import helper
from .command import Command

class HelloCommand(Command):

    def process(self):
        logmessage = helper.LogMessage(self.get_command_text())

