import logging
import random
import urllib.request
import time

from constants import NEWS_WEBS, DRILL_TIMEOUT, DEFAULT_HEADER
from logger import init_logger
from web_utils import get_proxy, prepare_proxy, request_general


class TinyDrill:
    def __init__(self):
        self.proxy_list = []
        self.webs = NEWS_WEBS
        self.burks = []

    def init_drill(self):

        logging.info("Start Logger initialization...")
        init_logger()
        logging.info("Logger initialization completed")

        #logging.info("Start getting proxies...")
        #self.proxy_list = get_proxy()
        #logging.info(f"Proxy retrieved: {self.proxy_list}")

    def kai_drill(self, web_url):
        logging.info(f"Starting drill for {web_url}")
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            prepare_proxy(proxy)
        soup = request_general(url=web_url, headers=DEFAULT_HEADER, is_gzipped=True, name_tag=web_url)
        coverpage_news = soup.find_all('h2', class_='articulo-titulo')
        print(soup)

    def kai_bai(self):
        pass


if __name__ == '__main__':
    drill = TinyDrill()
    drill.init_drill()
    drill.kai_drill(drill.webs[0])
