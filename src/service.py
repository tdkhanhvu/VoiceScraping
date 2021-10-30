import requests
from bs4 import BeautifulSoup

import pandas as pd
import os.path

ROOT_URL = "https://www.voiptroubleshooter.com/open_speech/"
MAIN_PAGE = "index.html"

DATA_FOLDER = "./data/"
AUDIO_FOLDER = DATA_FOLDER + "audios/"
META_FILE = DATA_FOLDER + "metadata.csv"
META_COLS = ["Name", "Gender", "Format", "Sample Rate", "Dialect"]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get(ROOT_URL + MAIN_PAGE, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

languages = soup.find(id="LayerMain").find_all("ul")[1].find_all("li")

if os.path.isfile(META_FILE):
    metadata_df = pd.read_csv(META_FILE)
else:
    metadata_df = pd.DataFrame(columns=META_COLS)


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
            audio_link = items[0].find("a")["href"]
            audio_name = items[0].find("a").text
            audio_gender = items[1].find("div").text
            audio_format = items[2].find("div").text
            audio_rate = items[3].find("div").text
            audio_dialect = items[4].text

            # only update this record in meta if it does not exist
            if len(metadata_df.query("Name == @audio_name")) == 0:
                new_row = {
                    META_COLS[0]: audio_name,
                    META_COLS[1]: audio_gender,
                    META_COLS[2]: audio_format,
                    META_COLS[3]: audio_rate,
                    META_COLS[4]: audio_dialect
                }

                metadata_df = metadata_df.append(new_row, ignore_index=True)
                print(audio_link, audio_name, audio_gender, audio_format, audio_rate, audio_dialect)

            # only write if this audio does not exist
            audio_file = AUDIO_FOLDER + audio_name
            if not os.path.isfile(audio_file):
                r = requests.get(ROOT_URL + audio_link, allow_redirects=True, headers=headers)

                with open(audio_file, 'wb') as f:
                    f.write(r.content)


metadata_df.to_csv(META_FILE, index=False)