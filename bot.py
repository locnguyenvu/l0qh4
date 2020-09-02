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

    """ CallbackQuery handler """
    from l0qh4.telegram.callbackquery.dispatcher import Dispatcher as CallbackQueryDispatcher
    dp.add_handler(CallbackQueryHandler(CallbackQueryDispatcher()))

    """ Command handler """
    from l0qh4.telegram.command.hello_command import HelloCommand 
    dp.add_handler(CommandHandler('hello', HelloCommand()))

    from l0qh4.telegram.command.today_command import TodayCommand
    dp.add_handler(CommandHandler('td', TodayCommand()))
    dp.add_handler(CommandHandler('today', TodayCommand(show_detail=True)))

    from l0qh4.telegram.command.thismonth_command import ThismonthCommand
    dp.add_handler(CommandHandler('tm', ThismonthCommand()))
    dp.add_handler(CommandHandler('thismonth', ThismonthCommand(show_detail=True)))

    from l0qh4.telegram.command.selectslcategory_command import  SelectSlCategoryCommand
    dp.add_handler(CommandHandler('mlc',SelectSlCategoryCommand()))

    from l0qh4.telegram.command.log_command import LogCommand
    dp.add_handler(CommandHandler('log', LogCommand()))

    from l0qh4.telegram.command.piechart_command import PieChartCommand
    dp.add_handler(CommandHandler('pc', PieChartCommand()))

    from l0qh4.telegram.command.logdetail_command import LogDetailCommand
    dp.add_handler(CommandHandler('d', LogDetailCommand()))

    """ Message handler """
    from l0qh4.telegram.directmessage.dispatcher import Dispatcher as DirectMessageDispatcher
    directmessaged_dispatcher = DirectMessageDispatcher(chatgroup_ids=os.getenv('TELEGRAM_LOGGING_GROUP_ID'))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), directmessaged_dispatcher))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
