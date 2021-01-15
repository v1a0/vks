from flex_loger import logger
import requests as req
from exceptions import *
from typing import Dict, List, Any


class APIBot:
    @logger.catch
    def __init__(self, tokens: List[str], proxy=None):
        if proxy is None:
            proxy = {}

        self.proxy = proxy  # proxy settings
        self.method = ''  # method for request
        self.params = {}  # parameters for request
        self.token = ''
        self._tokens_ = []
        self._tokens_default_ = []
        self.__set_tokens__(tokens)

    @logger.catch
    def __set_tokens__(self, tokens):
        tokens = [token for token in tokens if self.verify_api_token(token)]
        if not tokens:
            raise NoValidTokens

        self.token = tokens[0]  # API token
        self._tokens_ = tokens[1:] if len(tokens) > 1 else []  # tokens for popping in next_token
        self._tokens_default_ = tokens  # all tokens ever

    @logger.catch
    def next_token(self):
        if self._tokens_:
            self.token = self._tokens_.pop(0)

    @logger.catch
    def reset(self):
        if self._tokens_default_.__len__() > 0:
            self.token = self._tokens_default_[0]
            self._tokens_ = self._tokens_default_[1:]

    @logger.catch
    def verify_api_token(self, token: str) -> bool:
        """
        Verifying API Token
        :param token: API token
        :returns Bool: if valid return True else False
        """
        result_ = self.request(method='users.get?', params={'user_ids': ['1'], 'fields': ['photo_max_orig']},
                               token=token)

        if result_.get('error'):
            # need error_code
            return False

        else:
            return True

    @logger.catch
    def request(self, method: str, params: Dict[str, Any], token=None) -> Dict[str, Any]:
        """
        Sending request to VK API with selected method and params
        and parsing servers answer
        :returns JSON-like dict
        """
        if token is None:
            token = self.token

        parameters = ''
        for (parameter, values) in params.items():
            if type(values) == list:
                parameters += f"{parameter}={','.join(map(str, values))}&"  # map(str, value) stringifies list items
            else:
                parameters += f"{parameter}={values}&"

        request_ = f'https://api.vk.com/method/{method}?{parameters}' \
                   f'access_token={token}&' \
                   f'v=5.126'

        result = req.get(request_, proxies=self.proxy).json()

        if result.get('error'):
            if result.get('error').get('error_code') == 6:  # too many requests
                return self.request(token=token, method=method, params=params)

            elif result.get('error').get('error_msg') == 30: # page closed
                if self._tokens_:
                    self.next_token()
                return self.request(token=self.token, method=method, params=params)

        self.reset()
        return result
