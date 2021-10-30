import requests
from bs4 import BeautifulSoup

from Audio import AudioScraper
from MetaDataManager import MetaDataManagerScraper
from Language import Language
from Utils import UtilsScraper 

from Service import Service

class ServiceScraper(Service):
    def __init__(self):
        self.AudioClass = AudioScraper

    def process(self):
        self.meta_manager = MetaDataManagerScraper(UtilsScraper.DATA_FOLDER)

        page = requests.get(UtilsScraper.ROOT_URL + UtilsScraper.MAIN_PAGE, headers=UtilsScraper.HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

        for language in languages:
            language_item = Language(language)
            audios = language_item.get_audios(UtilsScraper.ROOT_URL, UtilsScraper.HEADERS)

            for audio in audios:
                self.process_audio(audio.find_all("td"))

        self.meta_manager.save()