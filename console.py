from dotenv import load_dotenv
load_dotenv()

import click
import os
import l0qh4

from pick import pick
from l0qh4.spending.log import Log as SpendingLog
from l0qh4.use_cases import spending_log as uc_sl

@click.group()
def console():
    pass

@console.command('initdb')
def initdb():
    dbengine = l0qh4.get('db').engine()
    base = l0qh4.core.Base
    base.metadata.create_all(dbengine)

@console.command('asltc')
def assign_spending_log_to_category():
    sl_repository = l0qh4.factory('spendinglog_repository')
    unassigned = sl_repository.find_all(entity_class=SpendingLog, spending_category_id=None)
    for log in unassigned:
        lcuc = uc_sl.ListProposedCategoryUseCase()
        categories = lcuc.execute(log)
        categories.append({"id": -1, "name": "..."})

        selected = pick(categories, log.get_subject(), indicator='=>', options_map_func=lambda c: c.get('name'))
        if selected[0].get('id') == -1:
            categories = lcuc.execute(log, {"listall": True})
            selected = pick(categories, log.get_subject(), indicator='=>', options_map_func=lambda c: c.get('name'))
        
        acuc = uc_sl.AssignCategoryUseCase()
        acuc.execute(log, {"category_id": selected[0].get('id')})
        print("lid#{} - {} >> {}".format(log.get_id(), log.get_subject(), selected[0].get('name')))

if __name__ == '__main__':
    console()
