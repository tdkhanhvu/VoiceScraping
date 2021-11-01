class Utils():
    ROOT_URL = ""
    MAIN_PAGE = ""

    DATA_FOLDER = ""
    AUDIO_FOLDER = ""

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class UtilsScraper(Utils):
    ROOT_URL = "https://www.voiptroubleshooter.com/open_speech/"
    MAIN_PAGE = "index.html"

    DATA_FOLDER = "./data/"
    AUDIO_FOLDER = DATA_FOLDER + "audios/"
