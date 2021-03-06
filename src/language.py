import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

class Language():
    """A class to handle the BeautifulSoup object scraped from a language"""
    def __init__(self, language:ResultSet) -> None:
        self.language = language

    def get_audios(self, root_url:str, headers:str) -> ResultSet:
        """Get all audios from this language"""
        a_object = self.language.find("a")

        language_name = a_object.text
        language_link = a_object["href"]
        print(language_name)

        language_page = requests.get(root_url + language_link, headers=headers)
        language_soup = BeautifulSoup(language_page.content, "html.parser")
        
        audios = language_soup.find("table").find("table").find_all("tr")

        # remove header
        audios.pop(0)

        return audios

   