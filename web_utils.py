import logging
import time
import urllib.request
import zlib
from socket import timeout

import requests
from bs4 import BeautifulSoup as bs, BeautifulSoup

from constants import TEST_PING_URL, PROXY_LIST_LENGTH, TEST_PING_TIMEOUT, DRILL_TIMEOUT


def get_free_proxy_list():
    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def prepare_proxy(proxy):
    proxy_header = {
        'http': proxy,
        'https': proxy,
    }
    proxy_support = urllib.request.ProxyHandler(proxy_header)
    authinfo = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_support, authinfo,
                                         urllib.request.CacheFTPHandler)
    urllib.request.install_opener(opener)


def get_proxy():
    proxy_list = get_free_proxy_list()
    good_proxy_list = []
    for i, proxy in enumerate(proxy_list):
        try:
            prepare_proxy(proxy)
            urllib.request.urlopen(url=TEST_PING_URL, timeout=TEST_PING_TIMEOUT)
            good_proxy_list.append(proxy)
            if len(good_proxy_list) == PROXY_LIST_LENGTH:
                break
        except:
            continue
    return good_proxy_list


def request_general(url, request_type='GET', headers=None, is_gzipped=False, name_tag="", resp_form=False):
    if headers is None:
        headers = {}
    tic = time.perf_counter()
    try:
        request_message = urllib.request.Request(url=url, headers=headers, method=request_type)
        with urllib.request.urlopen(request_message, timeout=DRILL_TIMEOUT) as response_message:
            if is_gzipped:
                response_message = zlib.decompress(response_message.read(), 16 + zlib.MAX_WBITS)
            if resp_form:
                return response_message
            soup = BeautifulSoup(response_message, features="html.parser")
    except Exception as err:
        if type(err) == timeout:
            logging.error(f'{request_type} url timeout: [{name_tag}] {err}')
        else:
            logging.error(f'{request_type} url failed: [{name_tag}] {err}')
        return None
    toc = time.perf_counter()
    logging.debug(f'Request {request_type}... [url: {url}]. Time taken:\t{toc - tic:0.4f}s')
    return soup


if __name__ == '__main__':
    print(get_proxy())
