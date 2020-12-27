from classes import Database
from flex_loger import logger
from typing import List

db: Database = Database(path='db/hidden_friends.db')


@logger.catch
def save_friends(parent_id: int = None, friends: List[int] = None, hidden_friends: List[int] = None):
    """
    Saving data about friends into db
    :param parent_id: id of target
    :param friends: detected friends of target
    :param hidden_friends: detected hidden friends of target
    :return:
    """
    if parent_id is None:
        parent_id = 0

    if friends is None:
        friends = []

    if hidden_friends is None:
        hidden_friends = []

    for friend in friends:
        insert_if_not_into(parent_id=parent_id, friend=friend, hidden='False')

    for friend in hidden_friends:
        insert_if_not_into(parent_id=parent_id, friend=friend, hidden='True')


@logger.catch
def insert_if_not_into(parent_id: int, friend: int, hidden: str):
    """
    Checking isn't record about friend already added into db, if it is not inserting
    :param parent_id: target id
    :param friend: friend id
    :param hidden: hidden status as str(bool)
    :return:
    """
    already_exist = db.select(table_name='friendship', select=['parent'],
                              where={'parent': parent_id, 'child': friend, 'hidden': hidden})

    if not already_exist:
        db.insert_or_replace(table_name='friendship', rows={
            'parent': parent_id,
            'child': friend,
            'hidden': hidden,
        })


@logger.catch
def table_init():
    """
    Initialization of necessary tables for module
    """

    db.create_table(
        table_name='friendship',
        rows={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'parent': 'INTEGER',
            'child': 'INTEGER',
            'hidden': 'TEXT',
        })


table_init()
