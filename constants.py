LOG_FILE_NAME = 'logging.txt'
LOG_FORMAT_SIMPLE = '%(asctime)s %(levelname)s : %(message)s'
LOG_FORMAT_FULL = "%(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s"

NEWS_WEBS = [
    'https://english.elpais.com/'
]

TEST_PING_TIMEOUT = 0.5
TEST_PING_URL = "http://www.google.ca"
PROXY_LIST_LENGTH = 5

DEFAULT_HEADER = {
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',

    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
}
DRILL_TIMEOUT = 5

