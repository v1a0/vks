from classes import APIBot
from flex_loger import logger
from typing import List, Any


@logger.catch
def get_online(users_ids: List[Any], bot: APIBot) -> List[int]:
    """
    Getting list of ids, returns list of online ids
    :param users_ids: List[str]
    :param bot: APIBot
    :return: List[int]
    """

    req = bot.request(method='users.get', params={
        'user_ids': users_ids,
        'fields': ['online']
    })

    if req.get('error'):
        logger.error("No valid ids")
        return []

    online_list = []
    responses = req.get("response")

    for response in responses:
        if response.get("online") == 1:
            online_list.append(response.get("id"))

    return online_list


@logger.catch
def get_online_friends(user_id: int, bot: APIBot) -> List[int]:
    """
    Getting user id, returns list ids of online friends
    :param user_id: int
    :param bot: APIBot
    :return: List[int]
    """

    req = bot.request(method='friends.get', params={
        'user_id': user_id
    })

    if req.get('error'):
        logger.error("No valid ids")
        return []

    responses = req.get("response")

    friends = responses.get("items")

    if not friends:
        logger.warning(f"No friends for {user_id}")
        return []

    return get_online(friends, bot)
