import requests
from bs4 import BeautifulSoup

import pandas as pd
import os.path

from Audio import Audio

ROOT_URL = "https://www.voiptroubleshooter.com/open_speech/"
MAIN_PAGE = "index.html"

DATA_FOLDER = "./data/"
AUDIO_FOLDER = DATA_FOLDER + "audios/"
META_FILE = DATA_FOLDER + "metadata.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get(ROOT_URL + MAIN_PAGE, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

if os.path.isfile(META_FILE):
    metadata_df = pd.read_csv(META_FILE)
else:
    metadata_df = pd.DataFrame(columns=Audio.Headers)


for language in languages:
    a_object = language.find("a")

    language_name = a_object.text
    language_link = a_object["href"]

    language_page = requests.get(ROOT_URL + language_link, headers=headers)
    language_soup = BeautifulSoup(language_page.content, "html.parser")
    
    audios = language_soup.find("table").find("table").find_all("tr")

    # remove header
    audios.pop(0)

    print(language_name)

    for audio in audios:
        items = audio.find_all("td")

        # skip empty lines
        if (items[0].find("a") is not None):
            audio_item = Audio.parse(items)

            # only update this record in meta if it does not exist
            if len(metadata_df.query("Name == @audio_item.name")) == 0:
                new_row = audio_item.create_row()

                metadata_df = metadata_df.append(new_row, ignore_index=True)
                audio_item.print()

            # only write if this audio does not exist
            audio_file = AUDIO_FOLDER + audio_item.name
            if not os.path.isfile(audio_file):
                r = requests.get(ROOT_URL + audio_item.link, allow_redirects=True, headers=headers)

                with open(audio_file, 'wb') as f:
                    f.write(r.content)


metadata_df.to_csv(META_FILE, index=False)