from settings import *
import vk_api_lite as api
import sqlite_requests as db
import time
import datetime


@logger.catch
def sleep(func):
    """
    Decorator for requests delay
    Waiting (60-delta) seconds after function is done
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        delay_time = start_time - time.time()
        time.sleep(delay_time if delay_time > 0 else REQ_FREQUENCY)

    return wrapper


@logger.catch
def none2zero(any_val):
    return any_val if any_val is not None else 0


@logger.catch
def user_data_parser(user_data, data_time):
    """
        Parsing user's data and sending it into DB
        logging results
    """

    db.insert_and_update_user_data(
        uid=user_data.get('id'),
        time=data_time,
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        is_closed=user_data.get('is_closed'),
        online=none2zero(user_data.get('online')),
        sex=user_data.get('sex'),
        photo=user_data.get('photo_max_orig'),
        mobile=none2zero(user_data.get('online_mobile')),
        os=none2zero(user_data.get('online_app'))
    )

    msg = f"[{user_data.get('id')}] {user_data.get('first_name')} {user_data.get('last_name')} " \
          f"{'Online' if user_data.get('online') is 1 else 'Offline'}"

    logger.info(msg)


@logger.catch
@api.verify_api_token
def loop():
    """
    If API_TOKEN valid starts logging
    """
    while True:
        main()


@logger.catch
@sleep
def main():
    """
    Getting, parsing and saving targets data
    """
    targets_data_json_list = api.get_alldata_json(ids=TARGETS, token=API_TOKEN)
    data_time = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    users = targets_data_json_list.get('response')
    for user_data in users:
        user_data_parser(user_data, data_time)

    logger.info(f'Scrapping loop finished, waiting (around) {REQ_FREQUENCY} sec for next...')


if __name__ == '__main__':

    logger.info(f"""Logging starting...
                TARGETS: {TARGETS}""")

    loop()

