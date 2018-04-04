import logging
import requests


logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):

        # You can iterate over ids, or get list of objects
        # from any API, or iterate throught pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you
        url = 'http://www.sin-say.com/ru/ru/shop-online/collection/t-shirts'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        s = requests.Session()
        response = s.get(url, headers=headers)
        if not response.ok:
            logger.error(response.text)
            return
            # then continue process, or retry, or fix your code
        else:
            # Note: here json can be used as response.json
            # save scrapped objects here
            # you can save url to identify already scrapped objects
            print(response.cookies)
            storage.write_data([url + '\t' + response.text.replace('\n', '')])
