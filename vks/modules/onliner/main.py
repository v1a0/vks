from classes import APIBot, Status
import datetime
import modules.onliner.db_connector as dbc
from flex_loger import logger


@logger.catch
def main(users_ids: [str], bot: APIBot):
    """
    Running main module process
    """
    status = Status(module_name='onliner')
    status.restarting()
    data = bot.request(method='users.get', params={
        'user_ids': users_ids,
        'fields': ['sex', 'online', 'photo_max_orig', 'online_mobile']
    })
    time_data = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

    if data.get('error'):
        status.failed()
        logger.error(data.get('error').get('error_msg'))
        return

    if data.get('response'):
        status.processing()
        for user_data in data.get('response'):
            user_data['time'] = time_data
            user_data['is_closed'] = str(user_data['is_closed'])
            dbc.save_user_data(user_data=user_data)

        status.success()

    else:
        status.failed()
        logger.error(f"No answer for {users_ids}...")
