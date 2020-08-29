from dotenv import load_dotenv
load_dotenv()

import click
import os
import l0qh4

from pick import pick
from l0qh4.container import ConsoleContainer
from l0qh4.spending.service.listproposedcategories_service import ListProposedCategoriesService
from l0qh4.spending.service.maplogtocategory_service import MapLogToCategoryService
from l0qh4.repository.spendinglog_repository import SpendingLogRepository

container = ConsoleContainer()
container.config.db.url.from_env('DATABASE_URL')

@click.group()
def console():
    pass

@console.command('initdb')
def initdb():
    dbengine = l0qh4.get('db').get_engine()
    ormmodel = l0qh4.shared.orm_model.OrmModel
    ormmodel.metadata.create_all(dbengine)

@console.command('mlc')
def assign_spending_log_to_category():
    sl_repository = SpendingLogRepository(l0qh4.get('db'))
    lsservice = ListProposedCategoriesService()
    mlcservice = MapLogToCategoryService()
    unmaplogs = sl_repository.find_all(spending_category_id = None)
    for log in unmaplogs:
        print(f"{log.get_id()} - {log.get_subject()}")
        categories = lsservice.execute(log) 
        categories.append({"id": -1, "name": "..."})
        selected = pick(categories, log.get_subject(), indicator='=>', options_map_func=lambda c: c.get('name'))
        if selected[0].get('id') == -1:
            categories = lsservice.execute(log, {"list_all": True})
            selected = pick(categories, log.get_subject(), indicator='=>', options_map_func=lambda c: c.get('name'))

        mlcservice.execute(log, int(selected[0].get('id')))

if __name__ == '__main__':
    console()
