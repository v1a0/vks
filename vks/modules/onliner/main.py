from classes import APIBot, Status
import datetime
import modules.onliner.db_connector as dbc
import modules.onliner.friends_online as friends
from flex_loger import logger
from multiprocessing import Process


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
            # For each target id
            # Adding data to main dict
            friends_online = friends.get_online_friends(user_id=user_data['id'], bot=bot)
            user_data['time'] = time_data
            user_data['is_closed'] = str(user_data['is_closed'])
            user_data['friends_online'] = friends_online

            # Saving data
            dbc.save_user_data(user_data=user_data)
            dbc.save_user_online(user_data=user_data)

            logger.info(f"[{user_data.get('id')}] {user_data.get('first_name')} {user_data.get('last_name')} - "
                        f"{'Online' if user_data.get('online') == 1 else 'Offline'}")

            # Running friends scrapping
            process = Process(target=scrap_friends, args=(friends_online, bot))  # running module
            process.start()

        status.success()

    else:
        status.failed()
        logger.error(f"No answer for {users_ids}...")


@logger.catch
def scrap_friends(friends_ids: [str], bot: APIBot):
    data = bot.request(method='users.get', params={
        'user_ids': friends_ids,
        'fields': ['sex', 'photo_max_orig', 'online_mobile']
    })

    if data.get('error'):
        logger.error(data.get('error').get('error_msg'))
        return

    if data.get('response'):
        for user_data in data.get('response'):
            user_data['is_closed'] = str(user_data['is_closed'])
            dbc.save_user_data(user_data=user_data)

