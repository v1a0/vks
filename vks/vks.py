from flex_loger import logger
from types import ModuleType
from classes import APIBot
import vk_api_lite as api
from settings import *
import time

BOTS: [APIBot] = []
TASKS: {ModuleType: [str]} = {}


@logger.catch
def sleep(func):
    """
    Decorator for loop's delay
    Waiting for a few seconds after run function again
    """
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(REQ_FREQUENCY)

    return wrapper


@logger.catch
@sleep
def init_bots(tokens_list, proxy, custom_proxy):
    """
    Initialize bots list

    :param custom_proxy: Proxy settings for special bot(s)
    :param tokens_list: List of tokens for bots
    :param proxy: Common proxy settings
    """
    for token in tokens_list:
        if api.verify_api_token(token):
            if custom_proxy.get(token):
                proxy = custom_proxy.get(token)

            BOTS.append(APIBot(token=token, valid=True, proxy=proxy))


@logger.catch
def init_tasks(targets, all_loads, load_excepts):
    """
    Tasks initialization
    TASKS: {
        module1: [id1, id2, id3],
        module2: [id1, id5]
        ...
    }
    :param targets: targets ids (sorry)
    :param all_loads: all modules - all possible load
    :param load_excepts: dict of modules witch have excluded targets
    """
    for load in all_loads:
        except_targets = load_excepts.get(load)

        if except_targets:
            TASKS[load] = [target for target in targets if target not in except_targets]
        else:
            TASKS[load] = targets


@logger.catch
def status_printer(results: [{ModuleType: bool}]):
    """
    Just printing results of modules work
    :param results: Results of modules work
    """
    if not results:
        return

    msg = f"\n{'='*10} RESULTS {'='*10}\n"
    for result in results:
        for (module, complete) in result.items():
            msg += f"{module.__name__}: {'Completed' if complete else 'Failed'}\n"
    logger.info(msg)


@logger.catch
@sleep
def main():
    """
    This module do:
        - Sets modules settings :     module.settings(ids, bot)
        - Running modules :           module.run()
        - Checking results :          module.is_done()
        - Final result contains in 'results' var as [ {module1: Bool}, {module2: Bool} ]
    """
    results: [{ModuleType: bool}] = []

    for (module, ids) in TASKS.items():
        if not ids:
            continue        # skips module if it have no attached ids

        try:
            if not module.ready():
                continue    # skips module if it is not ready

        except AttributeError as error:
            logger.error(error)
            continue        # skips module if it have no necessary attributes

        bots_for_task = [bot for bot in BOTS if bot.valid]
        is_complete = False

        while bots_for_task:                        # while (bots_for_task not empty)
            bot = bots_for_task[0]                  # sets new bot for a task

            try:                                    # try to use module
                module.settings(ids, bot)           # sending ids ans bot to module
                module.run()                        # running module
                is_complete = module.is_complete()  # result of module's work

            except AttributeError as error:         # if module has no one of necessary attributes
                logger.error(error)
                break                               # break the loop

            if is_complete:                         # if task is complete
                break                               # breaking loop
            else:                                   # if task is complete
                bots_for_task.pop(0)                # removing element

        results.append({module: is_complete})

    status_printer(results)


@logger.catch
def loop():
    while True:
        main()


if __name__ == '__main__':
    logger.info(f"""
    Logging starting...
    Settings of new monitoring session
    | Targets: {TARGETS_IDS}
    | API token: { f'<SET {len(API_TOKENS)}>' if API_TOKENS != ['__ENTER_YOUR_VK_API_TOKEN_HERE__'] else '<UNSET>'}
    | Proxy settings: {PROXY}
    +{'-' * 60}
    """)

    init_bots(API_TOKENS, PROXY, PROXY_FOR_BOT)
    init_tasks(TARGETS_IDS, MODULES, MODULES_EXCEPTS)
    loop()
