#
# free-proxy
# https://github.com/jundymek/free-proxy
# Licensed under the MIT license.
#
# this script is BASED ON https://github.com/jundymek/free-proxy/blob/master/fp/fp.py (2020)

import lxml.html as lx
import requests


class r_proxy:

    def __init__(self, timeout=0.5):
        self.timeout = timeout

    def get_proxy_list(self):
        try:
            page = requests.get('https://www.sslproxies.org')
            doc = lx.fromstring(page.content)
            tr_elements = doc.xpath('//*[@id="proxylisttable"]//tr')
            proxies = [f'{_proxy[0].text_content()}:{_proxy[1].text_content()}' for _proxy in tr_elements[1:100]]
            return proxies

        except requests.exceptions.RequestException as _error:
            print(_error)

    def get(self):
        print('[SECURE SETTINGS] Looking for a random HTTPS proxy... (100 in process)')
        proxy_list = self.get_proxy_list()
        working_proxy = None

        while True:
            for _proxy in proxy_list:
                proxies = {
                    'https': "https://" + _proxy,
                }
                try:
                    if self.check_if_proxy_is_working(proxies):
                        working_proxy = self.check_if_proxy_is_working(proxies)
                        print(f"[SECURE SETTINGS] {proxies['https']} SUCCESS!")
                        return working_proxy
                except requests.exceptions.RequestException:
                    print(f"[SECURE SETTINGS] {proxies['https']} FAILED")
                    continue
            break

        if not working_proxy:
            print('[SECURE SETTINGS] FAILED')
            self.get()

        return working_proxy

    def check_if_proxy_is_working(self, proxies):
        with requests.get('https://www.google.com', proxies=proxies, timeout=self.timeout, stream=True) as r:
            if r.raw.connection.sock:
                if r.raw.connection.sock.getpeername()[0] == proxies['https'].split(':')[1][2:]:
                    return {"https": f"{proxies['https']}"}

