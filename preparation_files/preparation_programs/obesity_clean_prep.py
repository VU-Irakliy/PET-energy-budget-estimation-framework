
import pandas as pd
import os
import numpy as np

from sklearn.preprocessing import LabelEncoder

def obesity_clean_preprocess():
    
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Obesity levels")
    # initial name was ObesityDataSet_raw_and_data_sinthetic, but we will consider it no synthetic
    obesity = pd.read_csv('obesity_dataset.csv', na_values=['?'])
    obesity = obesity.rename(columns={'FAVC': 'Frequent_high_cal', 'FCVC': 'Vegetables', 'NCP': 'How_many_meals', 'CAEC': 'between_meals', 'CH2O': 'Water_daily', 'SCC': 'Monitor_cals', 'FAF': 'Physical_activity_frequency', 'TUE': 'Tech_frequency', 'CALC': 'Alcohol_frequency', 'MTRANS': 'Transport', 'NObeyesdad': 'Obesity_level_original'}) 

    print(obesity.head())
    print(obesity.columns.to_list())
    obesity = obesity.dropna()
    # obesity[['Age', 'Vegetables', 'How_many_meals', 'Water_daily', 'Physical_activity_frequency' , 'Tech_frequency']]= obesity[['Age', 'Vegetables', 'How_many_meals', 'Water_daily', 'Physical_activity_frequency' , 'Tech_frequency']].astype('Int64')
    le = LabelEncoder()


    #Mapping: {'Insufficient_Weight': 0, 'Normal_Weight': 1, 'Obesity_Type_I': 2, 'Obesity_Type_II': 3, 'Obesity_Type_III': 4, 'Overweight_Level_I': 5, 'Overweight_Level_II': 6}
    obesity['Obesity_level'] = le.fit_transform(obesity['Obesity_level_original'])


    # print(obesity[['Obesity_level_original', 'Obesity_level']])
    print("Mapping:", dict(zip(le.classes_, le.transform(le.classes_))))
    
    os.chdir(owd)
    os.chdir("../preparation_files")


    
    
    obesity.to_csv('datasets/obesity.csv', index=False)

    

if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    obesity_clean_preprocess()