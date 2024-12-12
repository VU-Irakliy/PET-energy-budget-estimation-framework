
import pandas as pd
import os
import numpy as np



def german_clean_preprocess():

    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/German Credit")

    columns = [
    "status",
    "duration_in_month",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings_account_bonds",
    "present_employment_since",
    "installment_rate_in_percentage_of_disposable_income",
    "personal_status_and_sex",
    "other_debtors_guarantors",
    "present_residence_since",
    "property",
    "age_in_years",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "n_people_liable_maintenance",
    "telephone",
    "foreign_worker",
    "class"  # Target variable
    ]


    german = pd.read_csv("german.data",  delim_whitespace=True, header=None)

    german.columns = columns
    print(german.head())
    #we don't need to use fnlwgt, at it's used only to adjust for the sampling method used in the survey. Each record in the dataset represents multiple people in the population.


    # drop NA values from data set
    german= german.dropna()

    print(german['n_people_liable_maintenance'].unique())

    # adult_train.to_csv('', index=False)
    # print(adult_train.head())
   
    
    # os.chdir(owd)
    # os.chdir("../preparation_files")
    # print(os.getcwd())
    # german.to_csv('datasets/german.csv', index=False)








if __name__ == '__main__':
    # clean_adult()
    german_clean_preprocess()