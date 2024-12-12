
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_dataset():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Egyptian")
    #First, we handle regular csv file
    dataset = pd.read_csv('HCV-Egy-Data.csv', sep=',')
    
    new_column_names = {
        'Age ': 'age', 
        'Gender': 'gender', 
        'BMI': 'bmi', 
        'Fever': 'fever', 
        'Nausea/Vomting': 'nausea_vomiting', 
        'Headache ': 'headache',
        'Diarrhea ': 'diarrhea', 
        'Fatigue & generalized bone ache ': 'fatigue_bone_ache', 
        'Jaundice ': 'jaundice', 
        'Epigastric pain ': 'epigastric_pain', 
        'WBC': 'wbc', 
        'RBC': 'rbc', 
        'HGB': 'hgb', 
        'Plat': 'plat', 
        'AST 1': 'ast_1', 
        'ALT 1': 'alt_1',
        'ALT4': 'alt_4', 
        'ALT 12': 'alt_12', 
        'ALT 24': 'alt_24', 
        'ALT 36': 'alt_36', 
        'ALT 48': 'alt_48', 
        'ALT after 24 w': 'alt_after_24w',
        'RNA Base': 'rna_base', 
        'RNA 4': 'rna_4', 
        'RNA 12': 'rna_12', 
        'RNA EOT': 'rna_eot', 
        'RNA EF': 'rna_ef',
        'Baseline histological Grading': 'baseline_histological_grading', 
        'Baselinehistological staging': 'baseline_histological_staging'
    }
    dataset.rename(columns=new_column_names, inplace=True)
    print(dataset.info())
    print(dataset.head())
    print(dataset.columns)
    os.chdir(owd)
    os.chdir("../../preparation_files")
    dataset.to_csv(f'datasets/egyptian.csv', index=False)
    exit()
    label_encoder = LabelEncoder()
    dataset['label'] = label_encoder.fit_transform(dataset['label'])
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