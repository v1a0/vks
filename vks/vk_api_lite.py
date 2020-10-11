import requests as req
from settings import PROXY, API_TOKEN, logger


@logger.catch
def verify_api_token(func):
    """
    Decorator for verifying API_TOKEN
    Waiting (60-delta) seconds after function is done
    """

    def wrapper(*args, **kwargs):
        result_ = get_alldata_json('1', API_TOKEN)

        if result_.get('error'):
            logger.error(result_.get('error')['error_msg'])
            logger.error('Invalid API_TOKEN')
            breakpoint()

        else:
            return func(*args, **kwargs)

    return wrapper


@logger.catch
def get_user_as_json(ids, token, data):
    """
    Getting json form Vk API
    :returns list of data for correct ids (ignoring incorrect)
    """
    request_ = f'https://api.vk.com/method/users.get?' \
               f'user_ids={ids}&' \
               f'fields={data}&' \
               f'access_token={token}&' \
               f'v=5.124'

    result = req.get(request_, proxies=PROXY).json()

    return result


@logger.catch
def get_alldata_json(ids, token):
    result = get_user_as_json(ids, token, 'sex,online,photo_max_orig,online_mobile')
    return result


@logger.catch
def api_token_valid(api_token):
    result = get_alldata_json('1', api_token)

    if result.get('error'):
        logger.warning(result.get('error')['error_msg'])
        return False

    else:
        return True
