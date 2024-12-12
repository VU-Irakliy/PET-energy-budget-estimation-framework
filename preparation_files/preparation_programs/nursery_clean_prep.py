
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder


def nursery_clean_preprocess():
    ...


    #Cleaning
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Nursery")

    columns = ['parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health' ,'class']

    nursery = pd.read_csv("nursery.data", sep=",",names=columns,na_values=["?"], engine='python')

    nursery = nursery.dropna()
    print(nursery.head())
    print(nursery['class'].unique())
    
    le = LabelEncoder()

    # Fit and transform the 'class' column
    nursery['class_encoded'] = le.fit_transform(nursery['class'])


    print(nursery[['class', 'class_encoded']])
    print("Mapping:", dict(zip(le.classes_, le.transform(le.classes_))))
    nursery = nursery.drop('class', axis=1)
    
    os.chdir(owd)
    os.chdir("../preparation_files")
    
    
    nursery.to_csv('datasets/nursery.csv', index=False)





if __name__ == '__main__':
    nursery_clean_preprocess()