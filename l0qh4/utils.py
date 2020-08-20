import calendar
import re

from datetime import datetime

class DateTimeUtil:

    @staticmethod
    def datetime_range(timedesc:str) -> list:
        today = datetime.today()
        if timedesc == 'today':
            start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
            end_of_day = datetime(today.year, today.month, today.day, 23,59,59)
            return [start_of_day, end_of_day]
        if timedesc == 'thismonth':
            monthrange = calendar.monthrange(today.year, today.month)
            start_of_month = datetime(today.year, today.month, 1, 0, 0, 0)
            end_of_month = datetime(today.year, today.month, monthrange[1], 23, 59, 59)
            return[start_of_month, end_of_month]
        if timedesc == 'previousmonth':
            if today.month == 1:
                previousmonth = 12
                previousmonth_year = today.year - 1
            else:
                previousmonth = today.month - 1
                previousmonth_year = today.year
            monthrange = calendar.monthrange(previousmonth_year, previousmonth)
            start_of_month = datetime(previousmonth_year, previousmonth, 1, 0, 0, 0)
            end_of_month = datetime(previousmonth_year, previousmonth, monthrange[1], 23, 59, 59)
            return[start_of_month, end_of_month]
        return list()

class NumberUtil:

    @staticmethod
    def human_format(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

class StringUtil:

    @staticmethod
    def split_to_words(text: str):
        result = list()
        chunks = text.split(' ')
        regex_removenoncharacter = re.compile(r'\W')
        for chunk in chunks:
            pure_character = regex_removenoncharacter.sub('', chunk)
            if len(pure_character) == 0:
                continue
            result.append(pure_character)
        return result

