class Audio():
    Headers = ["Name", "Gender", "Format", "Sample Rate", "Dialect"]

    def __init__(self, link, name, gender, format, rate, dialect):
        self.link = link
        self.name = name
        self.gender = gender
        self.format = format
        self.rate = rate
        self.dialect = dialect

    def create_row(self):
        return {
            Audio.Headers[0]: self.name,
            Audio.Headers[1]: self.gender,
            Audio.Headers[2]: self.format,
            Audio.Headers[3]: self.rate,
            Audio.Headers[4]: self.dialect
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
