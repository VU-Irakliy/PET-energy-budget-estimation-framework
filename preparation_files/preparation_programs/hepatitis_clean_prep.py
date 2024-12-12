
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_dataset():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Hepatitis")
    #First, we handle regular csv file
    
    columns = [
        'class',
        'age', 
        'sex', 
        'steroid', 
        'antivirals', 
        'fatigue', 
        'malaise', 
        'anorexia', 
        'liver_big', 
        'liver_firm', 
        'spleen_palpable', 
        'spiders', 
        'ascites', 
        'varices', 
        'bilirubin', 
        'alk_phosphate', 
        'sgot', 
        'albumin', 
        'protime', 
        'histology'
    ]

    dataset = pd.read_csv("hepatitis.data", sep=",",names=columns,na_values=["?"], engine='python')
    dataset = dataset.dropna()
    print(dataset.head())
    print(dataset.info())
    print(dataset['class'].unique())
    

    os.chdir(owd)
    os.chdir("../../preparation_files")
    dataset.to_csv(f'datasets/hepatitis.csv', index=False)
    exit()
   

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    clean_dataset()