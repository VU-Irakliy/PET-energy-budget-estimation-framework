
import random
import string
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from codecarbon import EmissionsTracker
from termcolor import colored
import time
import sys



"""



"""








################################################################################################################################################################
"""
For ID project.
"""
def generate_id(length=10):
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choices(characters, k=length))
    return unique_id

################################################################################################################################################################
"""
For folder generation that belongs to the ID. If it exists, we generate a new ID.
"""
def create_unique_folder():
    #Create it in the output folder!
    while True:
        folder_id = generate_id()
        
        directory_name = f"./output/{folder_id}"
        
        if not os.path.exists(directory_name):
            try:
                os.makedirs(directory_name)
                print(f"Folder '{directory_name}' created successfully.")
                return folder_id
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            print(f"Folder '{directory_name}' already exists, generating a new ID...")
    
#######################################################################################
"""
Identify which attributes are categorical and which ones are continuous
"""
def categorize_columns(df, continuous_to_categorical):
        results = {}
        total_rows = len(df)
        dynamic_threshold = round(np.log(total_rows) / np.log(np.log(total_rows)) )
        if continuous_to_categorical != None:
            for column in df.columns:
                unique_count = df[column].nunique()
                if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2  or (column in continuous_to_categorical):
                    results[column] = 'Categorical'
                else:
                    # print(column)
                    # print(df[column].dtype)
                    results[column] = 'continuous'
        else:
            for column in df.columns:
                unique_count = df[column].nunique()
                if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2:
                    results[column] = 'Categorical'
                else:
                    # print(column)
                    # print(df[column].dtype)
                    results[column] = 'continuous'

        
        return results

################################################################################################################################################################
"""
Determine the threshold for synthetic data generation and the number of tuples generated in synthetic dataset. 
"""
def retrieve_values_for_pet(df, column_types):
    

    def find_max_unique_categorical(df, columns):
        
        # print("Attributes and their type:")
        # for key in column_types.keys():
        #     print(key, column_types[key])
        
        # print("\n")
        categorical_columns = {k: v for k, v in columns.items() if v == 'Categorical'}
        
        unique_counts = {column: df[column].nunique() for column in categorical_columns}
        
        max_unique_column = max(unique_counts, key=unique_counts.get)
        max_unique_value = unique_counts[max_unique_column]
        
        return max_unique_column, max_unique_value
    

    # try:
    #     df = pd.read_csv('preparation_files/datasets/'+ input_filename + '.csv')
    # except:
    #     print("File doesn't exist!")
    #     return False, False

    len_of_tuples = len(df)

    max_unique_column, max_unique_value = find_max_unique_categorical(df, column_types)
    print(f"\nThe categorical attribute with the most unique values is '{max_unique_column}' with {max_unique_value} unique values.")
    
    threshold = max_unique_value +  1
    print(f"Threshold for data synthesis generation is {threshold}.")
    return len_of_tuples, threshold

################################################################################################################################################################
"""
Launch CodeCarbon tracker for misc. Also avoid errors as much as possible.
"""
def tracker_launcher():
    count = 0
    while True:
        try:
            #With log_level, we have prints off!
            tracker = EmissionsTracker(log_level='error')

            return tracker
        except:
            print("\n Unexpected error. Trying again. \n")
            count += 1
        if count == 5:
            print('There is an unexpected error. Please try launching it again! If the issue persists, contact the developer!\n')
            exit()



################################################################################################################################################################
"""
Determine if possible known attributes are 1 list or 2 lists. If none of those, then the framework will stop working.
"""
def is_it_a_list(variable):
        if isinstance(variable, list):
            if all(isinstance(i, list) for i in variable):
                return 2 #List of Lists
            return 1 #List
        return 0 #Not a List

################################################################################################################################################################
"""
Perform necessary tasks depending on an outcome of the is_it_a_list function.
"""
def determine_the_list(input_cols, temp_df, secret):
    if is_it_a_list(input_cols) == 1:
        #Generate another list
        

        if input_cols != [col for col in input_cols if col in temp_df.columns]:
            ...
            print("Some of the columns were not found. Please, check for grammar!")
            sys.exit()
        
      
        return 1
        ...
    elif is_it_a_list(input_cols) == 0:
        ...
        print("\n possible_known_attributes is not a list or tuple(list of lists). Exiting the program")
        exit()
    else:
        for i in input_cols:
            for j in i:
                if j not in temp_df.columns:
                    print("Some of the columns were not found. Please, check for grammar!")
                    exit()
        return 0
        # return input_cols

################################################################################################################################################################