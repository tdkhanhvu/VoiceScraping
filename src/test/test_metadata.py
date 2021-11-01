import pandas as pd
from functools import reduce

PATH = "data/"
meta_audio_df = pd.read_csv(PATH + "metadata_audio.csv")
meta_sound_df = pd.read_csv(PATH + "metadata_sound_detector.csv")
meta_language_df = pd.read_csv(PATH + "metadata_language_detector.csv")

dfs = [meta_audio_df, meta_sound_df, meta_language_df]

df_final = reduce(lambda left,right: pd.merge(left,right,on='name'), dfs)

print(df_final)