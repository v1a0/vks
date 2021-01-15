from flex_loger import logger
from classes import Database
from typing import Dict, Any

db: Database = Database(path='db/onliner.db')


@logger.catch
def tables_init():
    """
    Initialization of necessary tables for module
    """
    db.create_table(
        table_name='online_log',
        rows={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'time': 'TEXT',
            'user_id': 'INTEGER',
            'online': 'INTEGER',
            'mobile': 'INTEGER',
            'os': 'TEXT',
            'friends_online': 'TEXT',
        },
        foreign_keys={'user_id': 'users("user_id")',}
    )

    db.create_table(
        table_name='users',
        rows={
            'user_id': 'INTEGER PRIMARY KEY UNIQUE',
            'first_name': 'TEXT',
            'last_name': 'TEXT',
            'is_closed': 'TEXT',
            'sex': 'INTEGER',
            'photo': 'TEXT',
        }
    )


@logger.catch
def save_user_data(user_data: Dict[str, Any]):
    """
    Inserting users data into db (if user does not exist) or updating (if user already exist)
    Saving online status
    """

    for key in ['online', 'mobile', 'os']:
        user_data[key] = 0 if not user_data.get(key) else user_data.get(key)

    already_exist = db.select(
        table_name='users',
        select=['user_id'],
        where={
            'user_id': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'is_closed': user_data.get('is_closed'),
            'sex': user_data.get('sex'),
            'photo': user_data.get('photo_max_orig'),
        })

    if not already_exist:
        db.insert_or_replace(
            table_name='users',
            rows={
                'user_id': user_data.get('id'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'is_closed': user_data.get('is_closed'),
                'sex': user_data.get('sex'),
                'photo': user_data.get('photo_max_orig'),
            })


def save_user_online(user_data: Dict[str, Any]):

    db.insert(  # or_rep?
        table_name='online_log', rows={
            'time': user_data.get('time'),
            'user_id': user_data.get('id'),
            'online': user_data.get('online'),
            'mobile': user_data.get('mobile'),
            'os': user_data.get('os'),
            'friends_online': user_data.get('friends_online'),
        })


tables_init()
