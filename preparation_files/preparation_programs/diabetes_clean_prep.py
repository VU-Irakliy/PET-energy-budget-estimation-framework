
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from dateutil import parser
from dateutil.parser import ParserError
def categorize_columns(df):
    results = {}
    total_rows = len(df)
    dynamic_threshold = round(np.log(total_rows) / np.log(np.log(total_rows)) )
    
    for column in df.columns:
        unique_count = df[column].nunique()
        if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2:
            results[column] = 'Categorical'
        else:
            # print(column)
            # print(df[column].dtype)
            results[column] = 'continuous'

    
    return results


'''

Diabetes dataset

'''

def clean_diabetes():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/diabetes")
    #First, we handle regular diabetes.csv
    diabetes = pd.read_csv('diabetic_data.csv', sep=',')
    #https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008 
    

    le = LabelEncoder()
    diabetes['readmitted'] = le.fit_transform(diabetes['readmitted'])
    print("Mapping:", dict(zip(le.classes_, le.transform(le.classes_))))
    
    for column in diabetes.columns:
        unique_values = diabetes[column].dropna().unique()
        nan_count = diabetes[column].isna().sum()
        if nan_count > 0:
            print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")

    diabetes = diabetes.drop('weight', axis=1)
    diabetes['age'] = diabetes['age'].str.replace('[\[\]\(\)]', '', regex=True)
    diabetes['race'] = diabetes['race'].replace('?', 'Unknown')

    diabetes= diabetes.drop('payer_code', axis=1)
    diabetes['medical_specialty'] = diabetes['medical_specialty'].replace('?', 'Unknown')
    for col in ['diag_1', 'diag_2', 'diag_3']:
        diabetes[col] = diabetes[col].replace('?', 'Unknown')

    diabetes['max_glu_serum'] = diabetes['max_glu_serum'].fillna('Unknown')
    diabetes['A1Cresult'] = diabetes['A1Cresult'].fillna('Unknown')
    #We don't need encounter_id or patient_nbr, because it will influence many things.
    diabetes = diabetes.drop(['encounter_id', 'patient_nbr'], axis = 1)
    diabetes = diabetes.apply(transform_column)
    # diabetes = diabetes.query("City != 'New York'")
    # Display the first few rows to verify changes
    
    print(diabetes.head(15))
    print(diabetes.columns)
    

    diabetes = diabetes[~diabetes['age'].map(is_date)]
    diabetes['diag_1'] = pd.to_numeric(diabetes['diag_1'], errors='coerce')
    diabetes = diabetes.dropna(subset=['diag_1'])
    
    diabetes['diag_2'] = pd.to_numeric(diabetes['diag_2'], errors='coerce')
    diabetes = diabetes.dropna(subset=['diag_2'])
    diabetes['diag_3'] = pd.to_numeric(diabetes['diag_3'], errors='coerce')
    diabetes = diabetes.dropna(subset=['diag_3'])
    def normalize_column(series):
        max_value = series.max()
        return series / max_value if max_value != 0 else series

    # Apply normalization
    diabetes['diag_1'] = normalize_column(diabetes['diag_1'])
    diabetes['diag_2'] = normalize_column(diabetes['diag_2'])
    diabetes['diag_3'] = normalize_column(diabetes['diag_3'])
    diabetes = diabetes.dropna()
    diabetes = diabetes.head(1000)
    print(diabetes.info())
   
    for column in diabetes.columns:
        try:
            # Attempt to calculate the product of the column
            product = diabetes[column].prod()
            print(f"Column '{column}' calculated successfully with product: {product}")
        except Exception as e:
            # Catch and print the error with the column name
            print(f"Error in column '{column}': {str(e)}")
    # Display the unique types
    # exit()
    os.chdir(owd)
    os.chdir("../../preparation_files")

    diabetes.to_csv('datasets/diabetes.csv', index=False)
    print('\n')
    df = pd.read_csv('datasets/diabetes.csv')
    column_types = categorize_columns(df)
    continuous_columns = [k for k, v in column_types.items() if v == 'continuous']
    for column in continuous_columns:
        try:
            # Attempt to calculate the product of the column
            product = df[column].prod()
            print(f"Column '{column}' calculated successfully with product: {product}")
        except Exception as e:
            # Catch and print the error with the column name
            print(f"Error in column '{column}': {str(e)}")







def is_date(value):
    try:
        parser.parse(value)
        return True
    except (ParserError, TypeError, ValueError):
        return False

# Filter DataFrame to keep only rows where 'mixed_column' is not of type str

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
    clean_diabetes()