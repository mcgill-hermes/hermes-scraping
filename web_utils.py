import logging
import time
import urllib.request
import zlib
import pandas as pd
from socket import timeout

import requests
from bs4 import BeautifulSoup as bs, BeautifulSoup

from constants import TEST_PING_URL, PROXY_LIST_LENGTH, TEST_PING_TIMEOUT, DRILL_TIMEOUT
from logger import init_logger


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
            print(response_message.read())
            if is_gzipped:
                response_message = zlib.decompress(response_message.read(), zlib.MAX_WBITS | 16)
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


def not_startswith(url, exception_list):
    for excep in exception_list:
        if url.startswith(excep):
            return False
    return True


def request_dashboard(url, template, exceptions):
    r = requests.get(url)
    b = BeautifulSoup(r.content, "html.parser")
    links = [link.get('href') for link in b.findAll('a')]
    links = set(links)
    prep_links = [link for link in links if link.startswith(template) and not_startswith(link, exceptions)]
    return prep_links


def request_content(url, type_class):
    r = requests.get(url)
    b = BeautifulSoup(r.content, "html.parser")
    body = b.find("div", {"class": type_class})
    return body.text if body is not None else None


def retrieving_nbc_news(category):
    nbc_url = 'https://www.nbcnews.com/' + category
    template_url = f'https://www.nbcnews.com/news/'
    exceptions_list = [template_url+'nbc-news-digital-editors']
    news_web_list = request_dashboard(nbc_url, template_url, exceptions_list)
    logging.info(f'Get {len(news_web_list)} news from {nbc_url}.')
    result = []

    for i in news_web_list:
        content = request_content(i, "article-body__content")
        if content is not None:
            result.append([i, category, content])
        time.sleep(0.33)

    return result


if __name__ == '__main__':
    init_logger()
    result = retrieving_nbc_news('world')
    df = pd.DataFrame(result, columns=['url', 'category', 'content'])
    for i in df['content']:
        print(i)