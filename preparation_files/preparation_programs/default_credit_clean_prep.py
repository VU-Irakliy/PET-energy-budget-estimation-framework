
import pandas as pd
import os
import numpy as np


def clean_default():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Default Credit")
    #First, we handle regular default_credit.csv
    default_credit = pd.read_excel('default of credit card clients.xls')
    default_credit = default_credit.rename(columns={'default payment next month': 'def_payment'})
    default_credit.columns = default_credit.columns.str.lower()

    print(default_credit.head())


    for column in default_credit.columns:
        unique_values = default_credit[column].dropna().unique()
        nan_count = default_credit[column].isna().sum()
        if nan_count > 0:
            print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    default_credit = default_credit.drop('id', axis= 1)
    default_credit = default_credit.head(4500)
    os.chdir(owd)
    os.chdir("../../preparation_files")

    default_credit.to_csv('datasets/default_credit.csv', index=False)
    
    

if __name__ == '__main__':
    # clean_adult()
    clean_default()