
import pandas as pd
import os
import numpy as np


def clean_indian():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Indian Liver")
    #First, we handle regular indian.csv
    column_names = [
        'age',
        'gender',
        'total_bilirubin',
        'direct_bilirubin',
        'alkphos',
        'sgpt',
        'sgot',
        'total_proteins',
        'albumin',
        'albumin_and_globulin_ratio',
        'is_patient'
    ]

    indian = pd.read_csv('Indian Liver Patient Dataset (ILPD).csv', sep=',', names=column_names)

    print(indian.head(15))
    # for column in indian.columns:
    #     unique_values = indian[column].dropna().unique()
    #     nan_count = indian[column].isna().sum()
    #     if nan_count > 0:
    #         print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    indian = indian.dropna()
    print(indian.info())
    indian = indian.head(1500)
    os.chdir(owd)
    os.chdir("../../preparation_files")

    indian.to_csv('datasets/indian.csv', index=False)
    
    
    

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column widt
    clean_indian()