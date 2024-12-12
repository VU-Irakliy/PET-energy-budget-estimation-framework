
import pandas as pd
import os
import numpy as np
from sklearn.impute import SimpleImputer

'''

This dataset has too many NaN in too many attributes.
I will perform automatic process that will fill NaNs
'''
def clean_support2():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Support2")

    support2 = pd.read_csv('support2.csv', sep=',')
    support2 = support2.drop('death', axis=1)
    print(support2.head(10))
    support2["hospdead"] = support2["hospdead"].astype(int)

    numeric_imputer = SimpleImputer(strategy='median')
    numeric_columns = support2.select_dtypes(include=['number']).columns
    support2[numeric_columns] = numeric_imputer.fit_transform(support2[numeric_columns])


    categorical_imputer = SimpleImputer(strategy='most_frequent')
    categorical_columns = support2.select_dtypes(include=['object']).columns
    support2[categorical_columns] = categorical_imputer.fit_transform(support2[categorical_columns])

    for column in support2.columns:
        unique_values = support2[column].dropna().unique()
        nan_count = support2[column].isna().sum()
        if nan_count > 0:
            print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    # support2 = support2.dropna()
    print(support2.head(10))
    print(len(support2))
    support2 = support2.dropna()
    print(len(support2))
    support2 = support2.head(5000)
    kee = ['sex','age', 'race', 'edu', 'charges', 'income', 'dzgroup', 'hospdead']
    print(len(support2.columns))
    print(support2.columns)
    
    os.chdir(owd)
    os.chdir("../../preparation_files")
    feats = [16, 26, 32, 36, 46]
    records = [[9105], [3474, 2572,	1162], [2210, 1488,1021], 
    [2011, 1472, 1173], [1510, 1045,509]]

    for i in range(0, len(feats)):
        num_features_to_drop = 61 - feats[i]
        for record in records[i]:
            cath_copy = support2.head(record)
            features_to_drop = [col for col in support2.columns if col not in kee][:num_features_to_drop]
            cath_copy = cath_copy.drop(columns=features_to_drop)
            cath_copy.to_csv(f'datasets/support2_{str(feats[i])}_{str(record)}.csv', index=False)
    
    # num_features_to_drop = 20
    # features_to_drop = [col for col in support2.columns if col not in kee][:num_features_to_drop]
    # support2_2 = support2.drop(columns=features_to_drop)
    # print(support2_2.info())
    # support2_2.to_csv('datasets/support2_2.csv', index=False)
    # num_features_to_drop = 30
    # features_to_drop = [col for col in support2.columns if col != 'hospdead'][:num_features_to_drop]
    # support2_2 = support2.drop(columns=features_to_drop)
    # print(support2_2.info())
    # support2_2.to_csv('datasets/support2_3.csv', index=False)



def normalize_column(series):
    return series / series.max() if series.max() != 0 else series

def find_extreme_values(df):
    for column in df.select_dtypes(include=[np.number]).columns:
        max_value = df[column].max()
        min_value = df[column].min()
        print(f"Column '{column}' - Max: {max_value}, Min: {min_value}")
def find_problematic_column(df):
    for column in df.select_dtypes(include=[np.number]).columns:
        try:
            product = df[column].prod()
            if np.isinf(product) or np.isnan(product):
                print(f"Warning: Product in column '{column}' resulted in {product}")
            else:
                print(f"Column '{column}' calculated successfully with product: {product}")
        except Exception as e:
            print(f"Error calculating product for column '{column}': {e}")

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column widt
    clean_support2()