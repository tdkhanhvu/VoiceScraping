import os

import requests

from MetaDataManager import MetaDataManagerScraper
from Utils import UtilsScraper

class Audio():
    def __init__(self, items):
        pass

    def create_row(self):
        return {}

    def print(self):
        pass

    def is_valid(items):
        return True


class AudioScraper(Audio):
    def __init__(self, items):
        self.link=items[0].find("a")["href"]
        self.name=items[0].find("a").text
        self.gender=items[1].find("div").text
        self.format=items[2].find("div").text
        self.rate=items[3].find("div").text
        self.dialect=items[4].text

        self.items = items


    def create_row(self):
        return {
            MetaDataManagerScraper.Headers[0]: self.name,
            MetaDataManagerScraper.Headers[1]: self.gender,
            MetaDataManagerScraper.Headers[2]: self.format,
            MetaDataManagerScraper.Headers[3]: self.rate,
            MetaDataManagerScraper.Headers[4]: self.dialect
        }

    def process(self):
        audio_file = UtilsScraper.AUDIO_FOLDER + self.name
        if not os.path.isfile(audio_file):
            r = requests.get(UtilsScraper.ROOT_URL + self.link, allow_redirects=True, headers=UtilsScraper.HEADERS)

            with open(audio_file, 'wb') as f:
                f.write(r.content)

    def print(self):
        print(self.link, self.name, self.gender, self.format, self.rate, self.dialect)

    def is_valid(items):
        return items[0].find("a") is not None
