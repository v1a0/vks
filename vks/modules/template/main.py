from flex_loger import logger
from classes import APIBot, Status


@logger.catch
def main(users_ids: [str], bot: APIBot):
    """
    Running main module process
    """
    status = Status
    status.processing()

    '<-- HERE WILL BE MAIN LOGIC OF YOUR MODULE -->'

    status.success()
    # status.failed()   # if it's failed

    pass
