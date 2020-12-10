import modules.template.local_vars as local
from flex_loger import logger
from classes import APIBot


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
def run():
    """
    Running main module process
    """
    pass
