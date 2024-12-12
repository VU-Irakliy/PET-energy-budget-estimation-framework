
import pandas as pd
import os
import numpy as np

"""
The purpose of the Adult dataset is to determine if each individual's income exceeds 50k.

The cleaning and preprocessing process of the datasets have been partially copied from Pepijn de Reus.
The code can be found in both cleaning.py and preprocessing.py .
https://github.com/PepijndeReus/Privacy-Enhancing-ML/tree/main/Data


"""

def clean_adult():
    ...


    #Cleaning
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Adult")

    columns = ["age", "type_employer", "fnlwgt", "education", "education_num","marital", "occupation", "relationship", "race","sex","capital_gain", "capital_loss", "hr_per_week","country", "income"]

    adult_train = pd.read_csv("adult.data", sep=",\s",names=columns,na_values=["?"], engine='python')

    

    #we don't need to use fnlwgt, at it's used only to adjust for the sampling method used in the survey. Each record in the dataset represents multiple people in the population.

    adult_train = adult_train.drop('education_num', axis=1)
    adult_train = adult_train.drop('fnlwgt', axis=1)

    # since only 1 entry for entire set, remove this column
    adult_train = adult_train[adult_train.country != 'Holand-Netherlands']

    # drop NA values from data set
    adult_train = adult_train.dropna()

    # adult_train.to_csv('', index=False)
    # print(adult_train.head())
    # print(adult_train.info())

    # columns = ["age", "type_employer", "fnlwgt", "education", "education_num","marital", "occupation", "relationship", "race","sex","capital_gain", "capital_loss", "hr_per_week","country", "income"]
    # adult_test = pd.read_csv("adult.test", sep=",\s",names=columns,na_values=["?"], engine='python')

    # # delete unnecessary columns
    # adult_test = adult_test.drop('education_num', axis=1)
    # adult_test = adult_test.drop('fnlwgt', axis=1)
    # adult_test['income'] = adult_test['income'].str.replace('<=50K.', '<=50K')
    # adult_test['income'] = adult_test['income'].str.replace('>50K.', '>50K')

    # drop NA values from data set
    # adult_test = adult_test.dropna()

    # # print(adult_test.head())
    # # print(adult_test.info())


    # adult_original = pd.concat([adult_train, adult_test]).reset_index(drop=True)
    # print(adult_original.head())
    # print(adult_original.info())
    
    os.chdir(owd)
    os.chdir("../preparation_files")
    
    adult_train.to_csv('datasets/Adult_train.csv', index=False)
    # adult_test.to_csv('datasets/Adult_test.csv', index=False)
    # adult_original.to_csv('datasets/Adult_original.csv', index=False)
    #After a bit of thinking, we will proceed with Adult_original only. Other files won't be necessary.







if __name__ == '__main__':
    clean_adult()
