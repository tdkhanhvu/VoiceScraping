import requests
from bs4 import BeautifulSoup

import pandas as pd
import os.path

from Audio import Audio

class Service():
    ROOT_URL = "https://www.voiptroubleshooter.com/open_speech/"
    MAIN_PAGE = "index.html"

    DATA_FOLDER = "./data/"
    AUDIO_FOLDER = DATA_FOLDER + "audios/"
    META_FILE = DATA_FOLDER + "metadata.csv"

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def load_meta_file(self):
        if os.path.isfile(Service.META_FILE):
            return pd.read_csv(Service.META_FILE)

        return pd.DataFrame(columns=Audio.Headers)

    def save_meta_file(self, metadata_df):
        metadata_df.to_csv(Service.META_FILE, index=False)

    def load_data(self):
        self.metadata_df = self.load_meta_file()

        page = requests.get(Service.ROOT_URL + Service.MAIN_PAGE, headers=Service.HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

        for language in languages:
            self.process_language(language)

        self.save_meta_file(self.metadata_df)

    def process_language(self, language):
        a_object = language.find("a")

        language_name = a_object.text
        language_link = a_object["href"]

        language_page = requests.get(Service.ROOT_URL + language_link, headers=Service.HEADERS)
        language_soup = BeautifulSoup(language_page.content, "html.parser")
        
        audios = language_soup.find("table").find("table").find_all("tr")

        # remove header
        audios.pop(0)

        print(language_name)

        for audio in audios:
            self.process_audio(audio)

    def process_audio(self, audio):
        items = audio.find_all("td")

        # skip empty lines
        if (items[0].find("a") is not None):
            audio_item = Audio.parse(items)
            self.update_metafile(audio_item)
            self.download_audio(audio_item)

    def update_metafile(self, audio_item):
        # only update this record in meta if it does not exist
        if len(self.metadata_df.query("Name == @audio_item.name")) == 0:
            new_row = audio_item.create_row()

            self.metadata_df = self.metadata_df.append(new_row, ignore_index=True)
            audio_item.print()

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