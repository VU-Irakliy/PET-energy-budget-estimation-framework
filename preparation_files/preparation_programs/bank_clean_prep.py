
import pandas as pd
import os
import numpy as np


def clean_bank_marketing():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Bank")
    #First, we handle regular bank.csv
    bank = pd.read_csv('bank.csv', sep=';')

    bank = bank.dropna()
    bank.rename(columns={'y': 'subscription'}, inplace=True)

    # unique_values = bank['subscription'].unique()
    # print(unique_values)

    bank['subscription'] = bank['subscription'].str.replace('no', '0')
    bank['subscription'] = bank['subscription'].str.replace('yes', '1')
    bank['contacted_before'] = bank['pdays'].apply(lambda x: 0 if x == -1 else 1)
    bank['pdays'] = bank['pdays'].replace(-1, 0)

    bank_full = pd.read_csv('bank-full.csv', sep=';')

    bank_full = bank_full.dropna()

    bank_full.rename(columns={'y': 'subscription'}, inplace=True)

    bank_full['subscription'] = bank_full['subscription'].str.replace('no', '0')
    bank_full['subscription'] = bank_full['subscription'].str.replace('yes', '1')
    bank_full['contacted_before'] = bank_full['pdays'].apply(lambda x: 0 if x == -1 else 1)
    bank_full['pdays'] = bank_full['pdays'].replace(-1, 0)

    print(bank.head())
    print(bank_full.head())
    print('\n')
    print(bank_full[(bank_full['pdays'] == -1) & (bank_full['subscription'] == 1)].head())

    # print('\n')
    # print(len(bank_full)) # 45211
    # bank_full['pdays'] = bank_full['pdays'].replace(-1, np.nan)
    # bank_full = bank_full.dropna()
    # print(len(bank_full)) # 8257
    #Meaning that we either replace into a binary or keep it with nan

    os.chdir(owd)
    os.chdir("../../preparation_files/datasets")

    print(len(bank_full.columns))
    print(len(bank_full))
    print(len(bank))
    # exit()
    # bank.to_csv('bank.csv', index=False)
    # bank_full.to_csv('bank-full.csv', index=False)
    kee = ['age', 'marital', 'job', 'housing', 'loan', 'balance', 'subscription'] 
    num_features_to_drop = 5
    features_to_drop = [col for col in bank_full.columns if col  not in kee][:num_features_to_drop]
    
    bank_full_2 = bank_full.drop(columns=features_to_drop)
    bank_full_2 = bank_full_2.head(35000)
    bank_full_2.to_csv('bank-full_2.csv', index=False)

    
    

if __name__ == '__main__':
    # clean_adult()
    clean_bank_marketing()