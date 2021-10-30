import requests
from bs4 import BeautifulSoup

import pandas as pd
import os.path

from Audio import Audio
from MetaDataManager import MetaDataManager
from Language import Language

class Service():
    ROOT_URL = "https://www.voiptroubleshooter.com/open_speech/"
    MAIN_PAGE = "index.html"

    DATA_FOLDER = "./data/"
    AUDIO_FOLDER = DATA_FOLDER + "audios/"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def load_data(self):
        self.meta_manager = MetaDataManager(Service.DATA_FOLDER)

        page = requests.get(Service.ROOT_URL + Service.MAIN_PAGE, headers=Service.HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

        for language in languages:
            language_item = Language(language)
            audios = language_item.get_audios(Service.ROOT_URL, Service.HEADERS)

            for audio in audios:
                self.process_audio(audio)

        self.meta_manager.save()

    def process_audio(self, audio):
        items = audio.find_all("td")

        # skip empty lines
        if (items[0].find("a") is not None):
            audio_item = Audio.parse(items)
            self.meta_manager.update(audio_item)
            self.download_audio(audio_item)

    def download_audio(self, audio_item):
        # only write if this audio does not exist
        audio_file = Service.AUDIO_FOLDER + audio_item.name
        if not os.path.isfile(audio_file):
            r = requests.get(Service.ROOT_URL + audio_item.link, allow_redirects=True, headers=Service.HEADERS)

            with open(audio_file, 'wb') as f:
                f.write(r.content)


if __name__ == "__main__":
    service = Service()
    service.load_data()