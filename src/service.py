import requests
from bs4 import BeautifulSoup

from audio import AudioScraper, AudioSoundDetector
from metadatamanager import MetaDataManagerScraper, MetaDataManagerSoundDetector
from language import Language
from utils import UtilsScraper 


class Service():
    def __init__(self):
        pass

    def process(self):
        self.meta_manager.save()

    def process_audio(self, items):
        if self.AudioClass.is_valid(items):
            audio_item = self.AudioClass(items)
            audio_item.process()
            self.meta_manager.update(audio_item)

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

        super().process()

class ServiceSoundDetector(Service):
    def __init__(self):
        self.AudioClass = AudioSoundDetector

    def process(self):
        print("Process")
        filenames = MetaDataManagerScraper(UtilsScraper.DATA_FOLDER).get_all_files()
        self.meta_manager = MetaDataManagerSoundDetector(UtilsScraper.DATA_FOLDER)

        print("Files:")
        print(filenames)

        for filename in filenames:
            items = {'name': filename}
            self.process_audio(items)

        super().process()