import os

import requests

import torch
torch.set_num_threads(1)

from utils import UtilsScraper

class Audio():
    """Base class to handle Audio objects"""
    def __init__(self, items:object, meta_class:'MetaDataManager') -> None:
        self.audio_path= UtilsScraper.AUDIO_FOLDER + self.name
        self.items = items
        self.MetaClass = meta_class

    def create_row(self) -> dict:
        """Create a new row to insert into metadata table"""
        return {}

    def process(self) -> None:
        """Process this audio item"""
        pass

    def print(self) -> None:
        """Print this audio item"""
        pass

    def is_valid(items) -> bool:
        """Check if the items object is valid"""
        return True

class AudioScraper(Audio):
    """Class to handle Audio object for Scraper"""

    def __init__(self, items:object, meta_class:'MetaDataManager') -> None:
        self.link=items[0].find("a")["href"]
        self.name=items[0].find("a").text
        self.gender=items[1].find("div").text
        self.format=items[2].find("div").text
        self.rate=items[3].find("div").text
        self.dialect=items[4].text

        super().__init__(items, meta_class)


    def create_row(self) -> dict:
        """Create a new row to insert into metadata table"""
        return {
            self.MetaClass.Headers[0]: self.name,
            self.MetaClass.Headers[1]: self.gender,
            self.MetaClass.Headers[2]: self.format,
            self.MetaClass.Headers[3]: self.rate,
            self.MetaClass.Headers[4]: self.dialect
        }

    def process(self) -> None:
        """Process this audio item"""
        if not os.path.isfile(self.audio_path):
            r = requests.get(UtilsScraper.ROOT_URL + self.link, allow_redirects=True, headers=UtilsScraper.HEADERS)

            with open(self.audio_path, 'wb') as f:
                f.write(r.content)

    def print(self) -> None:
        """Print this audio item"""
        print(self.link, self.name, self.gender, self.format, self.rate, self.dialect)

    def is_valid(items) -> bool:
        """Check if the items object is valid"""
        return items[0].find("a") is not None

class AudioSoundDetector(Audio):
    """Class to handle Audio object for Sound Detector"""
    read_audio = None
    get_speech_ts = None
    model = None

    def __init__(self, items:object, meta_class:'MetaDataManager') -> None:
        self.name = items['name']
        self.has_speech = False

        super().__init__(items, meta_class)

    def create_row(self) -> dict:
        """Create a new row to insert into metadata table"""
        return {
            self.MetaClass.Headers[0]: self.name,
            self.MetaClass.Headers[1]: self.has_speech
        }

    def process(self) -> None:
        """Process this audio item"""
        # lazy loading
        if self.__class__.read_audio is None:
            model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                        model='silero_vad',
                                        force_reload=True)

            (get_speech_ts,
            _, _, read_audio,
            _, _, _) = utils

            self.__class__.read_audio = read_audio
            self.__class__.get_speech_ts = get_speech_ts
            self.__class__.model = model

        try:
            wav = self.__class__.read_audio(self.audio_path)
            speech_timestamps = self.__class__.get_speech_ts(wav, self.__class__.model,
                                            num_steps=4)

            self.has_speech = len(speech_timestamps) > 0
            print("Detected Audio:", self.audio_path)
        except RuntimeError:
            print("Error detecting audio:", self.audio_path)

    
    def print(self) -> None:
        """Print this audio item"""
        print(self.name, self.has_speech)


class AudioLanguageDetector(Audio):
    """Class to handle Audio object for Language Detector"""
    read_audio = None
    get_language = None
    model = None

    def __init__(self, items:object, meta_class:'MetaDataManager') -> None:
        self.name = items['name']
        self.language = ""

        super().__init__(items, meta_class)

    def create_row(self) -> dict:
        """Create a new row to insert into metadata table"""
        return {
            self.MetaClass.Headers[0]: self.name,
            self.MetaClass.Headers[1]: self.language
        }


    def process(self) -> None:
        """Process this audio item"""
        # lazy loading
        if self.__class__.read_audio is None:
            model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                        model='silero_lang_detector',
                                        force_reload=True)

            get_language, read_audio = utils

            self.__class__.read_audio = read_audio
            self.__class__.get_language = get_language
            self.__class__.model = model

        try:
            wav = self.__class__.read_audio(self.audio_path)
            language = self.__class__.get_language(wav, self.__class__.model)

            self.language = language
            print(f"Detected Language:{self.language} for audio {self.audio_path}")
        except RuntimeError:
            print("Error detecting language:", self.audio_path)

    
    def print(self) -> None:
        """Print this audio item"""
        print(self.name, self.language)