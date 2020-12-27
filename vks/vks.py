from flex_loger import logger
from types import ModuleType
from classes import APIBot
from settings import *
import time
from multiprocessing import Process
from typing import Dict, List

BOT: APIBot
TASKS: Dict[ModuleType, List[str]] = {}
TIMEOUTS: Dict[ModuleType, List[str]] = {}


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
@sleep
def main():
    """
    This module do:
        - Sets modules settings :     module.settings(ids, bot)
        - Running modules :           module.run()
        - Checking results :          module.is_done()
        - Final result contains in 'results' var as [ {module1: Bool}, {module2: Bool} ]
    """

    for (module, ids) in TASKS.items():
        if not ids:
            continue  # skips module if it have no attached ids

        if not TIMEOUTS.get(module):
            TIMEOUTS[module] = 0

        elif TIMEOUTS.get(module) > time.time():
            continue

        logger.info(f"Running {module.__name__}...")
        process = Process(target=module.main, args=[ids, BOT])  # running module
        process.start()
        TIMEOUTS[module] = time.time() + MODULES_TIMEOUTS.get(module)


@logger.catch
def loop():
    while True:
        main()


if __name__ == '__main__':
    logger.info(f"""
    Logging starting...
    Settings of new monitoring session
    | Targets: {TARGETS_IDS}
    | API token: {f'<SET {len(API_TOKENS)}>' if API_TOKENS != ['__ENTER_YOUR_VK_API_TOKEN_HERE__'] else '<UNSET>'}
    | Proxy settings: {PROXY}
    +{'-' * 60}
    """)

    BOT = APIBot(tokens=API_TOKENS, proxy=PROXY)

    for ID in TARGETS_IDS:
        if type(ID) is int:
            ID = str(ID)

    init_tasks(TARGETS_IDS, MODULES, MODULES_EXCEPTS)
    loop()
