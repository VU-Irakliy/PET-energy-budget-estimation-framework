
import pandas as pd
import os
import numpy as np


def clean_catheterization():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Catheterization")
    cath = pd.read_csv('rhc.csv', sep=',')
    print(cath.info())
    cath = cath.rename(columns={
    'cat1': 'category1', 'cat2': 'category2', 'ca': 'cancer', 'sadmdte': 'adm_date', 'dschdte': 'discharge_date',
    'dthdte': 'death_date', 'lstctdte': 'last_con_dt',  'cardiohx': 'cardio_hist',
    'chfhx': 'chf_hist', 'dementhx': 'dementia_hx', 'psychhx': 'psych_hist', 'chrpulhx': 'pulm_hist',
    'renalhx': 'renal_hist', 'liverhx': 'liver_hist', 'gibledhx': 'gi_hist', 'malighx': 'malign_hist',
    'immunhx': 'immuno_hist', 'transhx': 'trans_hist', 'amihx': 'ami_hist',
     'edu': 'edu_years', 'surv2md1': '2m_survival', 'das2d3pc': 'das2d_3pc',
    'dnr1': 'dnr_status', 'ninsclas': 'insurance', 'resp': 'respiratory', 'card': 'cardiac',
    'neuro': 'neurologic', 'gastr': 'gastric', 'renal': 'renal_cond', 'meta': 'metabolic',
    'hema': 'hematologic', 'seps': 'sepsis', 'trauma': 'trauma_cond', 'ortho': 'ortho_cond', 'temp1': 'temperature' 
    
    })

    cath['adld3p'] = cath['adld3p'].fillna(0)
    cath['urin1'] = cath['urin1'].fillna(0)

    cath['category2'] = cath['category2'].fillna('None')
    cath = cath.drop(['death_date'], axis=1)
    cath = cath.apply(transform_column)
    # print(cath.head())
    # cath['adm_date'] = pd.to_datetime(cath['adm_date'], format='%Y%m%d', errors='coerce')
    # cath['discharge_date'] = pd.to_datetime(cath['discharge_date'], format='%Y%m%d', errors='coerce')
    # cath['last_con_dt'] = pd.to_datetime(cath['last_con_dt'], format='%Y%m%d', errors='coerce')
    for column in cath.columns:
        unique_values = cath[column].dropna().unique()
        nan_count = cath[column].isna().sum()
        if nan_count > 0:
            print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    cath = cath.dropna()
    print('\n')
    #TARGET IS DEATH
    #DATES cannot be converted. So, we're keeping them as they are
    print(cath.info())
    print(cath.head(10))
    print(len(cath))
    os.chdir(owd)
    os.chdir("../../preparation_files")
    print(len(cath.columns))
    # cath.to_csv('datasets/catheterization.csv', index=False)
    kee =['edu_years','sex', 'age', 'insurance', 'category1', 'cancer', 'death'] 

    feats = [61, 55, 47, 38, 29, 21]
    records = [[ 769, 521, 234], [2122, 1599, 553], [2345, 2000, 1479, 501], [2284, 2074, 1399, 584], [5531, 4095, 3419, 2131], [5734, 4236, 3541, 2111]]

    for i in range(0, len(feats)):
        num_features_to_drop = 61 - feats[i]
        for record in records[i]:
            cath_copy = cath.head(record)
            features_to_drop = [col for col in cath.columns if col not in kee][:num_features_to_drop]
            cath_copy = cath_copy.drop(columns=features_to_drop)
            cath_copy.to_csv(f'datasets/catheterization_{str(feats[i])}_{str(record)}.csv', index=False)

    # num_features_to_drop = 20
    # features_to_drop = [col for col in cath.columns if col not in kee][:num_features_to_drop]
    # cath_1 = cath.drop(columns=features_to_drop)
    # cath_1.to_csv('datasets/catheterization_1.csv', index=False)
    # num_features_to_drop = 40
    # features_to_drop = [col for col in cath.columns if col not in kee][:num_features_to_drop]
    # cath_2 = cath.drop(columns=features_to_drop)
    # cath_2.to_csv('datasets/catheterization_2.csv', index=False)
    # num_features_to_drop = 10
    # features_to_drop = [col for col in cath.columns if col not in kee][:num_features_to_drop]
    # cath_3 = cath.drop(columns=features_to_drop)
    # cath_3.to_csv('datasets/catheterization_3.csv', index=False)
    
def transform_column(col):
    if pd.api.types.is_string_dtype(col) and set(col.str.lower().unique()) == {'yes', 'no'}:
        return col.map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0})
    else:
        return col

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    clean_catheterization()