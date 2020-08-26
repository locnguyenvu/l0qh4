import os

from dotenv import load_dotenv
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Updater, Filters
from l0qh4.container import BotContainer

load_dotenv()

def main():
    container = BotContainer()
    container.config.db.url.from_env('DATABASE_URL')

    updater = Updater(
            token = os.getenv('TELEGRAM_BOT_TOKEN'),
            use_context = True)


    dp = updater.dispatcher

    callbackquery_handler = container.callbackquery_handler()
    dp.add_handler(CallbackQueryHandler(callbackquery_handler.listen))

    """ Command handler """
    command_handler = container.command_handler()
    from l0qh4.telegram.command.hello_command import HelloCommand 
    dp.add_handler(CommandHandler('hello', HelloCommand()))
    dp.add_handler(CommandHandler('log', command_handler.log))
    dp.add_handler(CommandHandler('pm', command_handler.pm))
    from l0qh4.telegram.command.today_command import TodayCommand
    dp.add_handler(CommandHandler('td', TodayCommand()))
    dp.add_handler(CommandHandler('today', TodayCommand(show_detail=True)))
    dp.add_handler(CommandHandler('tm', command_handler.tm))
    dp.add_handler(CommandHandler('mlc', command_handler.mlc))

    """ Message handler """
    message_handler = container.message_handler()
    message_handler.add_group_id(os.getenv('TELEGRAM_LOGGING_GROUP_ID'))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler.listen))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
