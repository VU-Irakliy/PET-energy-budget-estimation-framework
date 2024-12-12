
import pandas as pd
import os
import numpy as np



def productivity_clean_preprocess():
    ...


    #Cleaning
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Productivity Garment")
    productivity = pd.read_csv('garments_worker_productivity.csv', sep=',')
    print(productivity['actual_productivity'].unique())

    productivity = productivity.dropna()
    
    productivity['actual_productivity'] = productivity['actual_productivity'].apply(categorize_productivity)

    productivity['day_of_the_week'] = productivity['day']
    productivity['date'] = pd.to_datetime(productivity['date'])
    productivity['month'] = productivity['date'].dt.month
    productivity['day'] = productivity['date'].dt.day

    

    productivity = productivity.drop('date', axis=1)
    print(productivity.head())
    
    os.chdir(owd)
    os.chdir("../../preparation_files")
    
    
    productivity.to_csv('datasets/productivity_garment.csv', index=False)



def categorize_productivity(percentage):
    if percentage < 0.0:
        return  0 # Low
    elif percentage <= 0.75:
        return 1 #Medium
    else:
        return 2 #High



if __name__ == '__main__':
    # clean_adult()
    productivity_clean_preprocess()