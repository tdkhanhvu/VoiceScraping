from MetaDataManager import MetaDataManager

class Audio():
    def __init__(self, link, name, gender, format, rate, dialect):
        self.link = link
        self.name = name
        self.gender = gender
        self.format = format
        self.rate = rate
        self.dialect = dialect

    def create_row(self):
        return {
            MetaDataManager.Headers[0]: self.name,
            MetaDataManager.Headers[1]: self.gender,
            MetaDataManager.Headers[2]: self.format,
            MetaDataManager.Headers[3]: self.rate,
            MetaDataManager.Headers[4]: self.dialect
        }

    def parse(items):
        return Audio(
            link=items[0].find("a")["href"],
            name=items[0].find("a").text,
            gender=items[1].find("div").text,
            format=items[2].find("div").text,
            rate=items[3].find("div").text,
            dialect=items[4].text
        )

    def print(self):
        print(self.link, self.name, self.gender, self.format, self.rate, self.dialect)
