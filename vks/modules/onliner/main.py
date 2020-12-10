from classes import APIBot
import modules.onliner.local_vars as local
import datetime
import modules.onliner.db_connector as dbc
from flex_loger import logger


@logger.catch
def settings(users_ids: [str], bot: APIBot):
    """
    Settings for module
    :param users_ids: users ids
    :param bot:
    """
    local.users_ids = users_ids
    local.bot = bot
    dbc.tables_init()


@logger.catch
def is_complete() -> bool:
    """
    Is module complete successfully
    :return:
    """
    return local.is_complete


@logger.catch
def run():
    """
    Running main module process
    """
    data = local.bot.request(method='users.get', params={
        'user_ids': local.users_ids,
        'fields': ['sex', 'online', 'photo_max_orig', 'online_mobile']
    })
    time_data = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

    # NEED MORE COMMON CHECKING DATA BEFORE SET is_complete = True
    # what if only one user got an successfully response
    # but actually maybe not in this module

    if data.get('error'):
        local.is_complete = False
        logger.error(data.get('error').get('error_msg'))
        return

    if data.get('response'):
        local.is_complete = True
        for user_data in data.get('response'):
            user_data['time'] = time_data
            dbc.save_user_data(user_data=user_data)
        return

    else:
        local.is_complete = False
        logger.error(f"No answer for {local.users_ids}...")
