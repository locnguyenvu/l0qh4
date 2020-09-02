import l0qh4

from .command import Command
from ...spending.service.drawpiechart_service import DrawPieChartService

class PieChartCommand(Command):

    def process(self):
        params = self.get_messagecontent().split(' ')
        if len(params) == 1:
            timerange = 'thismonth'
        else:
            timerange = self._get_timerangealias(params[1])

        if timerange is None:
            self.reply('!e400 - invalid timerange')
            return
        
        drawchartservice = DrawPieChartService()
        piechart_path = drawchartservice.execute(timerange)
        self.bot.send_photo(
                self.effective_chat_id,
                open(piechart_path, 'rb'))
        

    def _get_timerangealias(self, timerange):
        if timerange in ['tm', 'thismonth']:
            return 'thismonth'
        if timerange in ['td', 'today']:
            return 'today'
        if timerange in ['pm', 'previousmonth']:
            return 'previousmonth'

        return None
