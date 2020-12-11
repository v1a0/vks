import modules.template.local_vars as local
from flex_loger import logger
from classes import APIBot
import time


@logger.catch
def sleep(func):
    """
    Decorator for requests delay
    Waiting (local.timeout) seconds after function has been run
    """
    def wrapper(*args, **kwargs):
        local.ready_after = time.time() + local.timeout
        func(*args, **kwargs)

    return wrapper


@logger.catch
def ready() -> bool:
    return time.time() >= local.ready_after


@logger.catch
def settings(users_ids: [str], bot: APIBot):
    """
    Settings for module
    :param users_ids: users ids
    :param bot:
    """
    local.users_ids = users_ids
    local.bot = bot


@logger.catch
def is_complete() -> bool:
    """
    Is module complete successfully
    :return:
    """
    return local.is_complete


@logger.catch
@sleep
def run():
    """
    Running main module process
    """
    '<-- HERE WILL BE MAIN LOGIC OF YOUR MODULE -->'
    pass


