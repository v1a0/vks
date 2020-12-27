import modules.hidden_friends.module_settings as settings
from modules.hidden_friends.module_classes import User
import modules.hidden_friends.db_connector as db
from multiprocessing import Process
from classes import APIBot, Status
from flex_loger import logger
from typing import List


@logger.catch
def main(users_ids: [str], bot: APIBot):
    """
    Running main module process
    """
    status = Status(module_name="hidden_friends")
    status.restarting()
    targets = preparing(users_ids, bot)

    if not targets:
        status.failed()
        return

    status.processing()

    for target in targets:
        if not target.is_closed:
            search = Process(target=find_friends, args=[target, bot])
            search.start()


@logger.catch
def preparing(users_ids: List[int], bot: APIBot):
    """
    Preparing module
    Checking profiles (users_ids) for vulnerability to attacks
    :return:
    """
    _return = []
    for user_id in users_ids:
        data = bot.request(method='friends.get', params={
            'user_id': user_id,
            'count': settings.max_friends,
        })

        if data.get('error'):
            logger.error(f"for id '{user_id}' failed\n{data.get('error').get('error_msg')}")
            if data.get('error').get('error_msg') == 30:
                _return.append(User(uid=user_id, is_closed=True, friends=[]))
            continue

        friends = data.get('response').get('items')
        _return.append(User(uid=user_id, is_closed=False, friends=friends, candidates=friends))

    return _return


@logger.catch
def find_friends(target: User, bot: APIBot, status=Status(module_name="hidden_friends")):
    """
    Looking for all friends and hidden friends of target
    And saving this data into db
    :param status:
    :param target: class User
    :param bot: class APIBot
    :return:
    """

    @logger.catch
    def get_friends_of(user_id: int) -> [int]:
        """
        Get list friends of user with id == user_id
        :param user_id: User id for get_friends request
        :return: List of (int) ids of friends
        """

        data = bot.request(method='friends.get', params={'user_id': user_id, 'count': settings.max_friends})
        response = data.get('response')

        if not response:
            return []

        return response.get('items')

    target_id = int(target.id)  # id of target
    checked_candidates = [int]  # list of already checked id's, to avoid the loops
    status.processing()

    for deepness in range(settings.deepness + 1):  # for each layer of deepness
        new_candidates = []     # here will be collecting candidates for a next searching layer

        for candidate in target.candidates:     # for each person who might be a friend
            candidate_id = int(candidate)       # id of potential friend
            checked_candidates.append(candidate_id)     # mark this id as already checked
            candidate_friends = get_friends_of(candidate)   # get friends of this peron
            new_candidates += candidate_friends     # add all person's friends to candidates list for next iteration

            if (target_id in candidate_friends) and (candidate_id not in target.friends):  # if target hiding this peron
                target.hidden_friends.append(candidate)     # add person to hidden_friends list

            log(deepness, target, target.candidates.index(candidate))

            save_friends = Process(target=db.save_friends, args=[int(target.id), target.friends, target.hidden_friends])
            save_friends.start()

        target.candidates = [x for x in new_candidates if x not in checked_candidates]  # filter already checked ids

    status.success()    # Task done successfully


@logger.catch
def log(deepness: int, target: User, done: int):
    """
    Logging status of module work
    Printing string like: "Deepness: 2, id: 1234, friends: 110, hidden friends: 10"
    :param deepness: deepness level of search
    :param target: has class User
    :param done: how many candidates already checked in this iteration (deepness level)
    """
    logger.info(f"Deepness: {deepness}, id: {target.id}, friends: {target.friends.__len__()}, "
                f"hidden friends: {target.hidden_friends.__len__()} | {done+1}/{target.candidates.__len__()}")
