# from yaml import parse
from commonInitObject import config
import delivery_sites_object as deliverys
from urllib3.exceptions import MaxRetryError
from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import argparse
import logging
import os
import pandas as pd
import datetime
import json
from os import write

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
other = re.compile(r'^https?://.+$')
is_root_path = re.compile(r'^/.+$')


def delivery_scraper(delivery_sites_uid, idx):
    host = config()['delivery_sites']['']['']
    logging.info('Beginning scraper for {}'.format(host))
    store_page = deliverys.StorePage(delivery_sites_uid, idx)
    stores = []
    for link in store_page.store_info:
        store = _fetch_store(_builder_link(link, host))
        if store != None:
            logging.info('store {} found and fetched'.format(link))
            stores.append(store)
        else:
            logging.info('store {} not available'.format(link))
    _save_store(stores,delivery_sites_uid, idx)

def _save_store(stores, delivery_sites_uid, idx):

    datasetstores = []

    for index in range(len(stores)):
        storee = stores[index]
        try:
            objstore = {
                'name': storee["name"],
                'latitude': storee["address"]["latitude"],
                'longitude': storee["address"]["longitude"],
            }
            try:
                objstore["city"] = storee["address"]["city"]
            except KeyError as e:
                objstore["city"] = "Mosquera"
            try:
                objstore["address"] = storee["address"]["streetName"] + " # " + storee["address"]["dependentAddress"] + " - " + storee["address"]["streetNumber"]
            except KeyError as e:
                try:
                    objstore["address"] = storee["address"]
                except KeyError as i:
                    objstore["address"] = "No Address Found"
                    print(i)
                print(e)
            datasetstores.append(objstore)
        except Exception as e:
            continue

    df_store = pd.DataFrame(datasetstores)

    df_store.to_csv('{}{}_.csv'.format(delivery_sites_uid,idx), sep=',', index=False , encoding='utf-8')

def _fetch_store(link):
    logging.info('Beginning fetching store {}'.format(link))
    try:
        response = requests.get(link)
        response.raise_for_status()
        try:
            store = BeautifulSoup(response.text, 'lxml').find('script', attrs={'id': '__NEXT_DATA__'}).get_text()
        except Exception as e:
            print(e)
            return None
        res_data = json.loads(store)['props']['initialState']['store']
        data_locations = res_data['details']
        if data_locations == []:
            return None
        else:
            return data_locations
    except (HTTPError, MaxRetryError) as e:
        logging.error('Error while trying to fetch article: {}'.format(e))
        return None

def _builder_link(link, host):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    elif other.match(link):
        return '{}/{}'.format(host, link)
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    delivery_sites_choices = list(config()['delivery_sites'].keys())
    index_choices = [str(x) for x in range(38)]
    parser.add_argument('delivery_site', help='The delivery site uid, must be one of: {}'.format(delivery_sites_choices), type=str, choices=delivery_sites_choices)
    parser.add_argument('index', help='index of file: data.json', type=str, choices=index_choices)
    args = parser.parse_args()
    delivery_scraper(args.delivery_site , args.index)
