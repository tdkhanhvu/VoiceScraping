import requests
from bs4 import BeautifulSoup

from audio import AudioScraper, AudioSoundDetector, AudioLanguageDetector
from metadatamanager import MetaDataManager, MetaDataManagerScraper, MetaDataManagerSoundDetector, MetaDataManagerLanguageDetector
from language import Language
from utils import UtilsScraper 


class Service():
    name = "Service"

    def __init__(self):
        self.MetaClass = MetaDataManager
        print("Started:", self.__class__.name)

    def process(self):
        self.meta_manager.save()

    def process_audio(self, items):
        if self.AudioClass.is_valid(items):
            audio_item = self.AudioClass(items, self.MetaClass)

            if not self.meta_manager.exist(audio_item):
                audio_item.process()
                self.meta_manager.update(audio_item)

class ServiceScraper(Service):
    name = "ServiceScraper"

    def __init__(self):
        super().__init__()
        self.MetaClass = MetaDataManagerScraper
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

        super().process()

class ServiceMLDetector(Service):
    name = "ServiceMLDetector"

    def __init__(self):
        super().__init__()

    def process(self):
        filenames = MetaDataManagerScraper(UtilsScraper.DATA_FOLDER).get_all_files()
        self.meta_manager = self.MetaClass(UtilsScraper.DATA_FOLDER)

        for filename in filenames:
            items = {'name': filename}
            self.process_audio(items)

        super().process()

class ServiceSoundDetector(ServiceMLDetector):
    name = "ServiceSoundDetector"

    def __init__(self):
        super().__init__()
        self.MetaClass = MetaDataManagerSoundDetector
        self.AudioClass = AudioSoundDetector


class ServiceLanguageDetector(ServiceMLDetector):
    name = "ServiceLanguageDetector"

    def __init__(self):
        super().__init__()
        self.MetaClass = MetaDataManagerLanguageDetector
        self.AudioClass = AudioLanguageDetector