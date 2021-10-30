import requests
from bs4 import BeautifulSoup

import os.path

from Audio import AudioScraper
from MetaDataManager import MetaDataManagerScraper
from Language import Language
from Utils import UtilsScraper 

class Service():
    def load_data(self):
        self.meta_manager = MetaDataManagerScraper(UtilsScraper.DATA_FOLDER)

        page = requests.get(UtilsScraper.ROOT_URL + UtilsScraper.MAIN_PAGE, headers=UtilsScraper.HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

        for language in languages:
            language_item = Language(language)
            audios = language_item.get_audios(UtilsScraper.ROOT_URL, UtilsScraper.HEADERS)

            for audio in audios:
                self.process_audio(audio)

        self.meta_manager.save()

    def process_audio(self, audio):
        items = audio.find_all("td")

        if AudioScraper.is_valid(items):
            audio_item = AudioScraper(items)
            self.meta_manager.update(audio_item)
            audio_item.process()

if __name__ == "__main__":
    service = Service()
    service.load_data()