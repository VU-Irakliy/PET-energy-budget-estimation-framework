
import pandas as pd
import os
import numpy as np
import py7zr
import chardet
from io import StringIO

def access_the_files():
    
    
    
    archive_path = './Rent classified/apartments_for_rent_classified_10K.7z'
    archive_path_2 = './Rent classified/apartments_for_rent_classified_100K.7z'
    extraction_path = './Rent classified'

    with py7zr.SevenZipFile(archive_path, mode='r') as z:
        z.extractall(path=extraction_path)

    with py7zr.SevenZipFile(archive_path_2, mode='r') as z:
        z.extractall(path=extraction_path)

def rent_clean_preprocess():
    ...
    with open('apartments_for_rent_classified_10K.csv', 'rb') as file:
        raw_data = file.read().decode('ISO-8859-1', errors='replace')

    df_10 = pd.read_csv(StringIO(raw_data), sep=';',on_bad_lines='skip', na_values=["?"],)

    print(df_10.head())
    print(df_10.info())
    df_10 = df_10.dropna()
    print(df_10.info())

    # with open('apartments_for_rent_classified_100K.csv', 'rb') as file:
    #     raw_data = file.read().decode('ISO-8859-1', errors='replace')

    # df_100 = pd.read_csv(StringIO(raw_data), sep=';',on_bad_lines='skip')

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data")
    # access_the_files()
    os.chdir("../data/Rent classified/")
    rent_clean_preprocess()