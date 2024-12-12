
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_dataset():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../../Bitcoin")
    #First, we handle regular csv file
    dataset = pd.read_csv('BitcoinHeistData.csv', sep=',')
    print(dataset.info())
    print(dataset.head())
    label_encoder = LabelEncoder()
    dataset['label'] = label_encoder.fit_transform(dataset['label'])
    print(dataset['label'].unique())

    #The Datasynthesizer breaks because of this column
    dataset = dataset.drop('count', axis=1)
    os.chdir(owd)
    os.chdir("../../preparation_files")
    print(len(dataset.columns))
    print(dataset.columns)
   
    #Having address in the dataset is too problematic!
    dataset = dataset.drop('address', axis=1)    


    dataset_1 = dataset.head(1000)
    dataset_1.to_csv(f'datasets/bitcoin.csv', index=False)
    for i in range(1, 6):
        dataset_1 = dataset.head(i * 10000)
        dataset_1.to_csv(f'datasets/bitcoin_{i}.csv', index=False)
    dataset_1 = dataset.head(5000)
    dataset_1.to_csv(f'datasets/bitcoin_0.csv', index=False)
    
     
if __name__ == '__main__':
    # pd.set_option('display.max_columns', None)  # Display all columns
    # pd.set_option('display.max_rows', None)     # Display all rows
    # pd.set_option('display.max_colwidth', None) # Display full column width
    clean_dataset()