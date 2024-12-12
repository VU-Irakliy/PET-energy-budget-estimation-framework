import sys
import os
import pandas as pd
import random
import numpy as np



def dataset_generator():
    target = 'target'
    maxi = 50
    num_categorical = random.randint(1, maxi)
    # num_categorical = 15
    num_continuous = random.randint(0, (maxi - num_categorical))
    cols = num_categorical + num_continuous
    aa = round(100000/(cols))
    num_rows = random.randint(500, aa)
    threshold = random.randint(15, 150)
    categorical_data = np.random.randint(1,threshold, size=(num_rows, num_categorical))
    
    # Generate random continuous data (as floats)
    continuous_data = np.random.randn(num_rows, num_continuous)
    
    # Generate random target variable (2 possible values: 0 or 1)
    target_data = np.random.randint(0, 2, size=(num_rows, 1))
    
    # Combine all data into a DataFrame
    data = np.hstack((categorical_data, continuous_data, target_data))
    column_names = [f'cat_{i+1}' for i in range(num_categorical)] + \
                   [f'num_{i+1}' for i in range(num_continuous)] + ['target']
    
    df = pd.DataFrame(data, columns=column_names)
    df.to_csv(f'random_{num_rows}_{cols}.csv', index=False)
    cat_names = [i for i in df.columns if 'cat' in i]
    return cat_names
    
    ...



if __name__ == '__main__':
    nums_to_categ = []
    # for i in range(0,50):
    cat_name = dataset_generator()
    # nums_to_categ.append(cat_name)
    # print(nums_to_categ)