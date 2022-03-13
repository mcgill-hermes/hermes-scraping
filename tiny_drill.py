import logging
import random
from datetime import datetime

import pandas as pd

from constants import NEWS_WEBS, DRILL_TIMEOUT, DEFAULT_HEADER
from logger import init_logger
from web_utils import prepare_proxy, retrieving_nbc_news


class TinyDrill:
    def __init__(self):
        self.proxy_list = []
        self.webs = NEWS_WEBS
        self.nuggets = []

    def init_drill(self):
        logging.info("Start Logger initialization...")
        init_logger()
        logging.info("Logger initialization completed")
        self.nuggets = []
        #logging.info("Start getting proxies...")
        #self.proxy_list = get_proxy()
        #logging.info(f"Proxy retrieved: {self.proxy_list}")

    def kai_drill_nbc(self):
        web_url = 'nbcnews'
        logging.info(f"Starting drill for {web_url}")
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            prepare_proxy(proxy)

        world = retrieving_nbc_news('world')
        tech = retrieving_nbc_news('tech')
        asian_america = retrieving_nbc_news('asian-america')
        result = pd.DataFrame(world + tech + asian_america, columns=['url', 'category', 'content'])
        self.nuggets.append([datetime.now(), result])
        result.to_csv('result.csv')
        print(result.shape)

    def kai_bai(self):
        pass


if __name__ == '__main__':
    drill = TinyDrill()
    drill.init_drill()
    drill.kai_drill_nbc()
