import os
import pandas as pd

class MetaDataManager():
    def __init__(self, data_folder, filename=""):
        self.meta_path = data_folder + filename
        self.load()

    def load(self):
        if os.path.isfile(self.meta_path):
            self.metadata =  pd.read_csv(self.meta_path)
        else:
            self.metadata = pd.DataFrame(columns=self.Headers)

    def save(self):
        self.metadata.to_csv(self.meta_path, index=False)

    def update(self, item):
        # only update this record in meta if it does not exist
        if not self.exist(item):
            new_row = item.create_row()
            print("Update:", new_row)
 
            self.metadata = self.metadata.append(new_row, ignore_index=True)

    def exist(self, item):
        return len(self.metadata.query("name == @item.name")) != 0

    def get_all_files(self):
        return self.metadata["name"].tolist()

class MetaDataManagerScraper(MetaDataManager):
    Headers = ["name", "gender", "format", "sample_rate", "dialect"]

    def __init__(self, data_folder, filename="metadata_audio.csv"):
        super().__init__(data_folder, filename)

class MetaDataManagerSoundDetector(MetaDataManager):
    Headers = ["name", "has_speech"]

    def __init__(self, data_folder, filename="metadata_sound_detector.csv"):
        super().__init__(data_folder, filename)

class MetaDataManagerLanguageDetector(MetaDataManager):
    Headers = ["name", "language"]

    def __init__(self, data_folder, filename="metadata_language_detector.csv"):
        super().__init__(data_folder, filename)
