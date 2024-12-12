
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_dataset():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Drugs")
    #First, we handle regular csv file
    
    columns = [
        'id',
        'age',
        'gender',
        'education',
        'country',
        'ethnicity',
        'nscore',
        'escore',
        'oscore',
        'ascore',
        'cscore',
        'impulsive',
        'ss',
        'alcohol',
        'amphet',
        'amyl',
        'benzos',
        'caff',
        'cannabis',
        'choc',
        'coke',
        'crack',
        'ecstasy',
        'heroin',
        'ketamine',
        'legalh',
        'lsd',
        'meth',
        'mushrooms',
        'nicotine',
        'semer',
        'vsa'
    ]

    dataset = pd.read_csv("drug_consumption.data", sep=",",names=columns,na_values=["?"], engine='python')
    
    dataset = dataset.head(10000)
    dataset = dataset.drop(['id', 'alcohol',
        'amphet',
        'amyl',
        'benzos',
        'caff',
        'cannabis',
        'choc',
        'coke',
        'crack',
        'ecstasy',
        'heroin',
        'ketamine',
        'legalh',
        'lsd',
        'meth',
        'mushrooms',
        'semer',
        'vsa'], axis=1)
    print(dataset.info())
    
    label_encoder = LabelEncoder()
    dataset['nicotine'] = label_encoder.fit_transform(dataset['nicotine'])
    dataset = dataset.dropna()
    print(dataset.head())
    print(dataset.info())

    os.chdir(owd)
    os.chdir("../../preparation_files")
    dataset.to_csv(f'datasets/drugs.csv', index=False)
    exit()
   

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    clean_dataset()