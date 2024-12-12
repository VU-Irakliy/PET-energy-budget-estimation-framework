
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_dataset():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Heart Failure")

    dataset = pd.read_csv('heart_failure_clinical_records_dataset.csv', sep=',')
    
    print(dataset.info())
    print(dataset.head())
    dataset.columns = dataset.columns.str.lower()
    print(dataset.columns)
   
    os.chdir(owd)
    os.chdir("../../preparation_files")
    dataset.to_csv(f'datasets/heart_failure.csv', index=False)
    exit()
    
    print(dataset['label'].unique())


    os.chdir(owd)
    os.chdir("../../preparation_files")
    print(len(dataset.columns))
    dataset_1 = dataset.head(1000)
    dataset_1.to_csv(f'datasets/bitcoin.csv', index=False)
    for i in range(1, 6):
        dataset_1 = dataset.head(i * 10000)
        dataset_1.to_csv(f'datasets/bitcoin_{i}.csv', index=False)
    dataset_1 = dataset.head(5000)
    dataset_1.to_csv(f'datasets/bitcoin_0.csv', index=False)
    
    # dataset.to_csv('datasets/catheterization.csv', index=False)
    # dataset.to_csv('datasets/catheterization_1.csv', index=False)

    exit()

    

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    clean_dataset()