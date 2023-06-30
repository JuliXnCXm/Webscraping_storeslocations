from logging import debug
from commonInitObject import config
import json


class DeliverySite:
    def __init__(self, delivery_sites_uid,idx):
        self.__config = config()['delivery_sites']['']
        self._data = None
        self._index = int(idx)
        self._delivery_sites_uid = delivery_sites_uid
        self.url_res = self.__config['']
        self._readingData()

    def _readingData(self):
        try:
            jsonFile = open('./data/data{}.json'.format(self._index), 'r')
            self._data = json.load(jsonFile)
            return self._data
        except Exception as e:
            debug(e)

class StorePage(DeliverySite):
    def __init__(self, delivery_sites_uid, idx):
        super().__init__(delivery_sites_uid,idx )

    @property
    def store_info(self):
        links_stores = []
        for info in self._data:
            links_stores.append(
                self.url_res + info['action'].split('%2F')[-1] + '/' + info['id'])

        return links_stores
