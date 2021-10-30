import os
from typing import List

import pandas as pd

from audio import Audio

class MetaDataManager():
    """Base class to handle Metadata"""
    def __init__(self, data_folder:str, filename:str="") -> None:
        self.meta_path = data_folder + filename
        self.load()

    def load(self) -> None:
        """Load the metadata file from the disk or create if not exists"""
        if os.path.isfile(self.meta_path):
            self.metadata =  pd.read_csv(self.meta_path)
        else:
            self.metadata = pd.DataFrame(columns=self.Headers)

    def save(self) -> None:
        """Save the metadata file to disk"""
        self.metadata.to_csv(self.meta_path, index=False)

    def update(self, item:Audio) -> None:
        """Update a new record in the metadata table"""
        # only update this record in meta if it does not exist
        if not self.exist(item):
            new_row = item.create_row()
            print("Update:", new_row)
 
            self.metadata = self.metadata.append(new_row, ignore_index=True)

    def exist(self, item:Audio) -> bool:
        """Check if a record exist in the metadata table"""
        return len(self.metadata.query("name == @item.name")) != 0

    def get_all_files(self) -> List[str]:
        """Return all file names in the metadata table"""
        return self.metadata["name"].tolist()

class MetaDataManagerScraper(MetaDataManager):
    """This class handle metadata for Scraper"""
    Headers = ["name", "gender", "format", "sample_rate", "dialect"]

    def __init__(self, data_folder:str, filename:str="metadata_audio.csv") -> None:
        super().__init__(data_folder, filename)

class MetaDataManagerSoundDetector(MetaDataManager):
    """This class handle metadata for Sound Detector"""
    Headers = ["name", "has_speech"]

    def __init__(self, data_folder:str, filename:str="metadata_sound_detector.csv") -> None:
        super().__init__(data_folder, filename)

class MetaDataManagerLanguageDetector(MetaDataManager):
    """This class handle metadata for Language Detector"""
    Headers = ["name", "language"]

    def __init__(self, data_folder:str, filename:str="metadata_language_detector.csv") -> None:
        super().__init__(data_folder, filename)
