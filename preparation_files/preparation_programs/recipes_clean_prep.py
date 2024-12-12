
import pandas as pd
import os
import numpy as np


def clean_recipes():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Recipes")
    #First, we handle regular recipes.csv
    recipes = pd.read_csv('Recipe Reviews and User Feedback Dataset.csv', sep=',')
    # no such a columns named num_records
    recipes = recipes.loc[:, ~recipes.columns.str.contains('^Unnamed')]
    
    recipes = recipes.dropna()
    recipes = recipes.drop('text', axis=1)
    recipes['best_score'] = recipes['best_score'].apply(classify_score)
    #these columns introduce potential bias
    recipes = recipes.drop(['user_id', 'comment_id', 'user_name'], axis=1)
    print(recipes.head(15))
    os.chdir(owd)
    os.chdir("../../preparation_files")

    recipes.to_csv('datasets/recipes.csv', index=False)
   
def classify_score(score):
    if score < 550:
        return 0 # 'Low'
    elif 550 <= score < 800:
        return 1 # 'Medium'
    else:
        return 2  #'High'


if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column widt
    clean_recipes()