import os

import requests

import torch
torch.set_num_threads(1)

from metadatamanager import MetaDataManagerScraper, MetaDataManagerSoundDetector
from utils import UtilsScraper

class Audio():
    def __init__(self, items):
        self.audio_path= UtilsScraper.AUDIO_FOLDER + self.name
        self.items = items

    def create_row(self):
        return {}

    def process(self):
        pass

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

        super().__init__(items)


    def create_row(self):
        return {
            MetaDataManagerScraper.Headers[0]: self.name,
            MetaDataManagerScraper.Headers[1]: self.gender,
            MetaDataManagerScraper.Headers[2]: self.format,
            MetaDataManagerScraper.Headers[3]: self.rate,
            MetaDataManagerScraper.Headers[4]: self.dialect
        }

    def process(self):
        if not os.path.isfile(self.audio_path):
            r = requests.get(UtilsScraper.ROOT_URL + self.link, allow_redirects=True, headers=UtilsScraper.HEADERS)

            with open(self.audio_path, 'wb') as f:
                f.write(r.content)

    def print(self):
        print(self.link, self.name, self.gender, self.format, self.rate, self.dialect)

    def is_valid(items):
        return items[0].find("a") is not None

class AudioSoundDetector(Audio):
    read_audio = None
    get_speech_ts = None
    model = None

    def __init__(self, items):
        self.name = items['name']
        self.has_speech = False

        super().__init__(items)

        if AudioSoundDetector.read_audio is None:
            model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                        model='silero_vad',
                                        force_reload=True)

            (get_speech_ts,
            _, _, read_audio,
            _, _, _) = utils

            AudioSoundDetector.read_audio = read_audio
            AudioSoundDetector.get_speech_ts = get_speech_ts
            AudioSoundDetector.model = model

    def create_row(self):
        return {
            MetaDataManagerSoundDetector.Headers[0]: self.name,
            MetaDataManagerSoundDetector.Headers[1]: self.has_speech
        }

    def process(self):
        try:
            wav = AudioSoundDetector.read_audio(self.audio_path)
            speech_timestamps = AudioSoundDetector.get_speech_ts(wav, AudioSoundDetector.model,
                                            num_steps=4)

            self.has_speech = len(speech_timestamps) > 0
            print("Detected Audio:", self.audio_path)
        except RuntimeError:
            print("Error detecting audio:", self.audio_path)

    
    def print(self):
        print(self.name, self.has_speech)