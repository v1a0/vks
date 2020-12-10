from flex_loger import logger
import modules.onliner.local_vars as local


@logger.catch
def tables_init():
    """
    Initialization of necessary tables for module
    """
    tables = [
        {
            'table_name': 'logging',
            'rows': {
                'id':       'INTEGER PRIMARY KEY AUTOINCREMENT',
                'time':     'TEXT',
                'user_id':  'INTEGER',
                'online':   'INTEGER',
                'mobile':   'INTEGER',
                'os':       'TEXT',
            },
            'foreign_keys': {
                'user_id': 'users("user_id")'
            },
        },
        {
            'table_name': 'users',
            'rows': {
                'user_id': 'VARCHAR(255) PRIMARY KEY',
                'first_name': 'TEXT',
                'last_name': 'TEXT',
                'is_closed': 'TEXT',
                'sex': 'INTEGER',
                'photo': 'TEXT',
            },
        },
    ]

    for table in tables:
        local.db.create_table(table)


@logger.catch
def save_user_data(user_data):
    """
    Inserting users data into db (if user does not exist) or updating (if user already exist)
    Saving online status
    """

    for key in ['online', 'mobile', 'os']:
        user_data[key] = 0 if not user_data.get(key) else user_data.get(key)

    data_about_user = {
            'table_name': 'users',
            'rows': {
                'user_id': user_data.get('id'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'is_closed': user_data.get('is_closed'),
                'sex': user_data.get('sex'),
                'photo': user_data.get('photo_max_orig'),
            }
    }
    local.db.insert_or_replace(data_about_user)

    data_about_online = {
            'table_name': 'logging',
            'rows': {
                'time': user_data.get('time'),
                'user_id': user_data.get('id'),
                'online': user_data.get('online'),
                'mobile': user_data.get('mobile'),
                'os': user_data.get('os'),
            }
    }
    local.db.insert_or_replace(data_about_online)

    logger.info(f"[{user_data.get('id')}] {user_data.get('first_name')} {user_data.get('last_name')} "
                f"{'Online' if user_data.get('online') == 1 else 'Offline'}")
