import re
import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pprint
from ..repository import SpendingLogRepository, UserRepository
from ..spending.categories import Categories as SpendingCategories
from ..spending.helper import LogMessage
from ..spending.log import Log
from ..users import Users
from ..utils import NumberUtil
from ..use_cases import (
        spending_log as uc_sl
)

class CommandHandler:

    def __init__(self, 
            spendinglog_repository: SpendingLogRepository, 
            spendingcategories: SpendingCategories,
            users: Users):
        self._users = users
        self._spendinglog_repository = spendinglog_repository
        self._spendingcategories = spendingcategories

    def is_authorized(self, update):
        if update.message is not None:
            tlg_username = update.message.from_user.username
        elif update.edited_message is not None:
            tlg_username = update.edited_message.from_user.username

        if tlg_username is None:
            return False
        return self._users.is_active(telegram_username = tlg_username)

    def hello(self, update, context):
        if not self.is_authorized(update):
            return
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "*Bot* nuôi heo của mỡ & nọng")

    def td(self, update, context):
        if not self.is_authorized(update):
            return
        todayspendinglog = self._spendinglog_repository.listall_intimerange('today')
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = 'Tổng cộng hôm nay: {:,}'.format(sum(list(map(lambda e: e.amount, todayspendinglog)))))

    def tm(self, update, context):
        if not self.is_authorized(update):
            return
        todayspendinglog = self._spendinglog_repository.listall_intimerange('thismonth')
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = 'Tổng cộng tháng này: {:,}'.format(sum(list(map(lambda e: e.amount, todayspendinglog)))))

    def pm(self, update, context):
        if not self.is_authorized(update):
            return
        todayspendinglog = self._spendinglog_repository.listall_intimerange('previousmonth')
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = 'Tổng cộng tháng trước: {:,}'.format(sum(list(map(lambda e: e.amount, todayspendinglog)))))

    def mlc(self, update, context):
        """ Map spending log with category """
        if update.message.reply_to_message is None:
            search_log_id_result = re.search(r'\d+', update.message.text)
            if search_log_id_result is None:
                return
            logid = int(search_log_id_result.group(0))
            log = self._spendinglog_repository.find(logid, entity_class=Log)
        else:
            log = self._spendinglog_repository.find_first(
                    telegram_message_id=update.message.reply_to_message.message_id,         
                    entity_class=Log)

        if log is None or log.get_category_id() != None:
            return
        usecase = uc_sl.ListProposedCategoryUseCase()
        proposed_categories = usecase.execute(log)

        keyboard = [
                [InlineKeyboardButton(f"{category['name']}", callback_data=f"mlc|logid={log.get_id()},categoryid={category['id']}")]
                for category in proposed_categories
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'{log.get_subject()}', reply_markup=reply_markup)

    def today(self, update, context):
        if not self.is_authorized(update):
            return
        todayspendinglog = self._spendinglog_repository.listall_intimerange('today')
        spendingrows = [
            '[{}] {:10.10} | {:<3}'.format(
                self._users.get_alias(telegram_username = log.created_by),
                log.subject, 
                NumberUtil.human_format(log.amount)) 
            for log in todayspendinglog
        ]
        totalamount = sum([ log.amount for log in todayspendinglog])
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = '\n'.join([
                        '```',
                        '\n'.join(spendingrows),
                        '{:=>20}'.format('='),
                        f'Tổng cộng hôm nay: {totalamount:,}',
                        '```'
                    ]),
                parse_mode = telegram.ParseMode.MARKDOWN_V2)

    def log(self, update, context):        
        if not self.is_authorized(update):
            return
        log_message = LogMessage(update.message.text)
        if not log_message.is_valid():
            return
        if update.message.forward_date != None:
            created_at  = update.message.forward_date
        else:
            created_at = None
        log = self._spendinglog_repository.add(
                subject = log_message.subject(),
                amount = log_message.amount(),
                payment_method = log_message.payment_method(),
                transaction_type = log_message.transaction_type(),
                created_by = update.message.from_user.username,
                telegram_message_id = update.message.message_id,
                created_at = created_at)
        context.bot.send_message(
            chat_id = update.effective_chat.id, 
            text = f'logid #{log.id}')


class MessageHandler(CommandHandler):

    __group_ids = []

    def add_group_id(self, group_id):
        self.__group_ids.append(int(group_id))

    def listen(self, update, context):
        if not self.is_authorized(update):
            return

        """ Log spending from group message """
        if update.message is not None:
            chat_info = update.message.chat
            if chat_info.type == 'group' and chat_info.id in self.__group_ids:
                self.log(update, context)
                return
            elif chat_info.type == 'private' and update.message.forward_date != None:
                self.log(update, context)
                return
    
        """ Edit existed spending log on message edited """
        if update.edited_message is not None:
            log_message = LogMessage(update.edited_message.text)
            if not log_message.is_valid():
                return
            spending_log = self.spendinglog_repository.find_first(
                    telegram_message_id = update.edited_message.message_id)
            if spending_log is None:
                return
            spending_log.subject = log_message.subject()
            spending_log.amount = log_message.amount()
            spending_log.payment_method = log_message.payment_method()
            spending_log.transaction_type = log_message.transaction_type()
            self.spendinglog_repository.update(spending_log)

class CallbackQueryHandler(CommandHandler):

    def listen(self, update, context):
        query = update.callback_query
        querydata = query.data.split('|')
        command = querydata[0]
        params = dict()
        for pinput in querydata[1].split(','):
            pairkv = pinput.split('=')
            params[pairkv[0]] = pairkv[1]

        query.answer()
        if command == 'mlc':
            self.mlc(query, **params)

    def mlc(self, query, logid, categoryid):
        catename = self._spendingcategories.get_name(int(categoryid))
        log = self._spendinglog_repository.find(logid, Log)

        usecase = uc_sl.AssignCategoryUseCase()
        usecase.execute(log, {"category_id": int(categoryid)})

        query.edit_message_text(text=f"{log.get_subject()} => {catename}")

