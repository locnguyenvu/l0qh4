import os
import l0qh4
import matplotlib.pyplot as plt

from ...repository.spendinglog_repository import SpendingLogRepository

class DrawPieChartService(object):

    def __init__(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))
        self._spendingcategories = l0qh4.get('spendingcategories')

    def execute(self, timerange: str = None):

        if timerange is None:
            timerange = 'today'

        logs = self._sl_repository.find_intimerange(timerange)

        grouped_by_cate = dict()
        grouped_by_cate[-1] = 0

        for log in logs:
            if not log.get_category_id():
                grouped_by_cate[-1] += log.get_amount()
                continue
            if log.get_category_id() not in grouped_by_cate:
                grouped_by_cate[log.get_category_id()] = log.get_amount()
            else:
                grouped_by_cate[log.get_category_id()] += log.get_amount()

        total = sum(grouped_by_cate.values())
        average =  total / len(grouped_by_cate)

        sizes = list()
        labels = list()
        explode = list()
        smallamounts = list() 
        smallsubjects = list()
        for key, value in grouped_by_cate.items():
            rate = int(value) / total * 100
            if (rate < 5):
                smallamounts.append(int(value))
                smallsubjects.append(self._spendingcategories.get_displayname(int(key)))
                continue
            labels.append(self._spendingcategories.get_displayname(int(key)))
            sizes.append(value)
            explode.append(0)
            
        sizes.append(sum(smallamounts))
        labels.append('\n'.join(smallsubjects))
        explode.append(0.1)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
       
        chartimg_path = os.path.join(l0qh4.RESOURCE_PATH, 'piechart.png')
        plt.title(f'Tổng cộng: {total:,}', loc="left", bbox={'facecolor':'0.8', 'pad':3})
        plt.savefig(chartimg_path)
        return chartimg_path
