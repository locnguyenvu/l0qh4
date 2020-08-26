from .command import Command

class HelloCommand(Command):

    def process(self):
        self.reply("*Bot* nuôi heo của mỡ & nọng")
