import requests as req
from flex_loger import logger


@logger.catch
def verify_api_token(token: str) -> bool:
    """
    Verifying API Token
    :param token: API token
    :returns Bool: if valid return True else False
    """
    result_ = request(token=token, method='users.get?', params={'user_ids': ['1'], 'fields': ['photo_max_orig']})

    if result_.get('error'):
        logger.error(result_.get('error')['error_msg'])
        logger.error('Invalid API_TOKEN')
        return False

    else:
        return True


@logger.catch
def request(token: str, method: str, params: dict, proxy=None) -> dict:
    """
    Sending request to VK API with selected method and params
    and parsing servers answer
    :returns JSON-like dict
    """
    if proxy is None:
        proxy = {}

    parameters = ''
    for (parameter, values) in params.items():
        parameters += f"{parameter}={','.join(values)}&"

    request_ = f'https://api.vk.com/method/{method}?{parameters}' \
               f'access_token={token}&' \
               f'v=5.124'

    result = req.get(request_, proxies=proxy).json()

    return result
