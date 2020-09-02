import l0qh4
import time
import threading

from .callbackquery import CallbackQuery
from ...spending.service.maplogtocategory_service import MapLogToCategoryService
from ...repository.spendinglog_repository import SpendingLogRepository

class MapSlCategoryCallbackQuery(CallbackQuery):

    def _onconstruct(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))
        self._scategories = l0qh4.get('spendingcategories')

    def execute(self, logid, categoryid):

        log = self._sl_repository.find_first(id = int(logid))
        categoryname = self._scategories.get_displayname(int(categoryid))

        mlcservice = MapLogToCategoryService()
        mlcservice.execute(log, int(categoryid))

        self.update.callback_query.edit_message_text(text=f"{log.get_subject()} => {categoryname}")
        deletmes = threading.Thread(target=self.clean, daemon=True)
        deletmes.start()

    def clean(self):
        time.sleep(10)
        self.update.callback_query.message.delete()
