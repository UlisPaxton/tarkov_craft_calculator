import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sys import exit


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class InterfaceCacher:

    def __init__(self, browser_class):
        self.browser = browser_class()
        self.cache = dict()

    def get_price(self, item_name):
        if item_name in self.cache.keys():
            return self.cache[item_name]
        else:
            price = self.browser.get_price(item_name)
            self.cache.update({item_name: price})
            return price


class CustomBrowser:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.get('https://tarkov-market.com/')
        self.session.headers = {'User-Agent': 'Mozilla/8.0 (Windows NT 05.0; Win64; x64; rv:68.0)'\
                                              ' Gecko/20100101 Firefox/68.0',
                                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Referer': 'https://tarkov-market.com/',
                                'Accept': 'application / json, text / plain, * / *',
                                }

    def get_price(self, item_name: str):
        url = f'https://tarkov-market.com/api/items?lang=en&search={item_name}\
                &tag=&sort=change24&sort_direction=desc&skip=0&limit=20'

        response = self.session.get(url)
        json_data = json.loads(response.text)

        try:
            price = int(json_data['items'][0]['avgDayPrice'])
            return price

        except KeyError:
            print('Не удалось получить цену, не найден элемент', item_name)
            exit()
        except IndexError:
            print('Не удалось получить цену, не найден элемент', item_name)
            exit()

