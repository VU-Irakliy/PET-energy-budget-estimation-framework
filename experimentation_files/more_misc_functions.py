
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
                
                # print(f"Folder '{directory_name}' created successfully.")
                return folder_id
                break
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            ...
            # print(f"Folder '{directory_name}' already exists, generating a new ID...")
    
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
    

    len_of_tuples = len(df)

    max_unique_column, max_unique_value = find_max_unique_categorical(df, column_types)
    # print(f"\nThe categorical attribute with the most unique values is '{max_unique_column}' with {max_unique_value} unique values.")
    
    threshold = max_unique_value +  1
    # print(f"Threshold for data synthesis generation is {threshold}.")
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
            exit()
        
      
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



def data_preparation_for_data_collection():



    # Dataset names in syn data but not in else: {'bitcoin_5', 'bitcoin_2', 'bitcoin_1', 'bitcoin', 'bitcoin_0', 'bitcoin_3', 'bitcoin_4', 
    # 'hcv', 'random_4463_14',  'random_3155_31', 'random_943_41', 'random_3169_20', 'random_742_45', 'random_1382_42', 'random_814_46', 'random_760_45'}
    


     # 'autism' 'german' 'nursery' 'obesity' 'productivity_garment' 'Adult_v2'
    # 'student-por' 'abalone' 'bank' 'bank-full' 'Adult_test_v2 '
    # 'Adult_train_v2' 'catheterization' 'coupons' 'default_credit '
    # 'support2_3' 'taiwan_bankrupt_3' 'indian' 'recipes' 'support2_2'
    # 'taiwan_bankrupt_2' 'catheterization_1' 'catheterization_2'
    # 'catheterization_3' 'bank-full_2' 'Adult_v2_(bank-full)'
    # 'bank-full_(Adult_v2)' 'drugs' 'egyptian' 'heart_failure' 'hepatitis'
    # 11 more catherizations
    # 31 more support2
    # 16 dropouts
    # 18 more taiwans
    # 34 randoms
    # """

    dropouts = ['marital_status', 'application_mode', 'application_order', 'course',
       'daytime/evening_attendance', 'previous_qualification',
       'previous_qualification_(grade)', 'nationality',
       'mother\'s_qualification', 'father\'s_qualification',
       'mother\'s_occupation', 'father\'s_occupation']
    randoms = [
    "cat_1", "cat_2", "cat_3", "cat_4", "cat_5", "cat_6", "cat_7", "cat_8", 
    "cat_9", "cat_10", "cat_11", "cat_12", "cat_13", "cat_14", "cat_15", 
    "cat_16", "cat_17", "cat_18", "cat_19", "cat_20", "cat_21", "cat_22", 
    "cat_23", "cat_24", "cat_25", "cat_26", "cat_27", "cat_28", "cat_29", 
    "cat_30", "cat_31", "cat_32", "cat_33", "cat_34", "cat_35", "cat_36", 
    "cat_37", "cat_38", "cat_39", "cat_40", "cat_41", "cat_42", "cat_43", 
    "cat_44", "cat_45", "cat_46", "cat_47", "cat_48", "cat_49", "cat_50", 
    "cat_51"
    ]
    filenames = ['autism','german','nursery','obesity','productivity_garment','Adult_v2',
    'student-por','abalone','bank','bank-full','Adult_test_v2',
    'Adult_train_v2','catheterization','coupons','default_credit',
    'support2_3','taiwan_bankrupt_3','indian','recipes','support2_2',
    'taiwan_bankrupt_2','catheterization_1','catheterization_2',
    'catheterization_3','bank-full_2','Adult_v2_(bank-full)',
    'bank-full_(Adult_v2)','drugs','egyptian','heart_failure','hepatitis',
    'catheterization_21_2111','catheterization_21_3541',
    'catheterization_21_4236','catheterization_21_5734',
    'catheterization_29_2131','catheterization_29_3419',
    'catheterization_29_4095','catheterization_29_5531',
    'catheterization_38_584','catheterization_38_1399',
    'catheterization_38_2074','catheterization_38_2284',
    'catheterization_47_501','catheterization_47_1479',
    'catheterization_47_2000','catheterization_47_2345',
    'catheterization_55_553','catheterization_55_1599',
    'catheterization_55_2122','catheterization_61_234',
    'catheterization_61_521','catheterization_61_769',
    'support2_16_9105',
    'support2_26_1162','support2_26_2572','support2_26_3474',
    'support2_32_1021','support2_32_1488','support2_32_2210',
    'support2_36_1173','support2_36_1472','support2_36_2011',
    'support2_46_509','support2_46_1045','support2_46_1510',
    'support2_46_2131','support2_46_3419','support2_16_234',
    'support2_16_521',
    'support2_16_769',
    'support2_26_553','support2_26_1599','support2_26_2122',
    'support2_32_501','support2_32_1479','support2_32_2000',
    'support2_32_2345','support2_36_584','support2_36_1399',
    'support2_36_2074','support2_36_2284','support2_46_4095',
    'support2_46_5531',
    'dropout','dropout_15_1142','dropout_15_2510',
    'dropout_15_3617','dropout_15_4424','dropout_20_1142','dropout_20_2510',
    'dropout_20_3617','dropout_20_4424','dropout_25_1142','dropout_25_2510',
    'dropout_25_3617','dropout_25_4424','dropout_30_2510','dropout_30_3617',
    'dropout_30_4424','taiwan_16_1246','taiwan_16_2500','taiwan_16_3012',
    'taiwan_16_4011','taiwan_26_743','taiwan_26_1272','taiwan_26_1999',
    'taiwan_26_3256','taiwan_26_4011','taiwan_30_793','taiwan_30_1592',
    'taiwan_30_2386','taiwan_30_3257','taiwan_51_1001','taiwan_51_1502',
    'taiwan_61_721','taiwan_61_1001','taiwan_65_500','random_507_34',
    'random_534_50','random_638_46','random_736_44','random_1711_27',
    'random_1810_39','random_1969_46','random_2003_43','random_2031_49',
    'random_2202_37','random_3109_30','random_1040_46','random_1071_41',
    'random_1407_30','random_1560_48','random_1905_35','random_2016_38',
    'random_2557_25','random_2705_33','random_2916_28','random_2998_14',
    'random_4308_18','random_7711_5','random_536_41','random_724_50',
    'random_800_43','random_867_50','random_1106_50','random_1270_47',
    'random_1614_50','random_2044_47','random_2123_41','random_2142_38',
    'random_764_50']

   
    nums_to_categ = [ 
        None, None, ['class_encoded'], None, ['day', 'month'], None,
         ['G1', 'G2'], None, ['day'], ['day'], None, 
         None, None,  None,['education', 'marriage'], 
        ['edu', 'prg6m', 'adlp'],   None , None , None, ['edu', 'prg6m', 'adlp'],
       None, None, None,
       None, ['day'], None,
       ['day'], ['nicotine'], ['baseline_histological_grading','baseline_histological_staging'], None, None
    ] +  [None] * 22 + [['edu', 'prg6m', 'adlp']] * 31 + [dropouts] * 16  + [None] * 18 + [randoms] * 34
    


   

    targets = [
        'class', 'class', 'class_encoded', 'Obesity_level', 'actual_productivity','income',
        'G3', 'age_category', 'subscription', 'subscription', 'income',
        'income', 'death', 'coupon_accepted', 'def_payment',
        'hospdead', 'bankrupt', 'is_patient',  'best_score',  'hospdead',
        'bankrupt', 'death', 'death',
        'death', 'subscription', 'income',
        'subscription', 'nicotine', 'baseline_histological_staging', 'death_event','class'
    ]  + ['death'] * 22 +  ['hospdead'] * 31 + ['target'] * 16 + ['bankrupt'] * 18 + ['target'] * 34



    
    print(len(filenames))
    print(len(nums_to_categ))
    print(len(targets))
    return filenames, nums_to_categ, targets
    

























"""GARBAGE"""



# def data_retrieval_for_more():



#     # Dataset names in syn data but not in else: {'bitcoin_5', 'bitcoin_2', 'bitcoin_1', 'bitcoin', 'bitcoin_0', 'bitcoin_3', 'bitcoin_4', 
#     # 'hcv', 'random_4463_14',  'random_3155_31', 'random_943_41', 'random_3169_20', 'random_742_45', 'random_1382_42', 'random_814_46', 'random_760_45'}
#     randoms = [
#     "cat_1", "cat_2", "cat_3", "cat_4", "cat_5", "cat_6", "cat_7", "cat_8", 
#     "cat_9", "cat_10", "cat_11", "cat_12", "cat_13", "cat_14", "cat_15", 
#     "cat_16", "cat_17", "cat_18", "cat_19", "cat_20", "cat_21", "cat_22", 
#     "cat_23", "cat_24", "cat_25", "cat_26", "cat_27", "cat_28", "cat_29", 
#     "cat_30", "cat_31", "cat_32", "cat_33", "cat_34", "cat_35", "cat_36", 
#     "cat_37", "cat_38", "cat_39", "cat_40", "cat_41", "cat_42", "cat_43", 
#     "cat_44", "cat_45", "cat_46", "cat_47", "cat_48", "cat_49", "cat_50", 
#     "cat_51"
#     ]
#     filenames_1 = ['bitcoin_5', 'bitcoin_2', 'bitcoin_1', 'bitcoin', 'bitcoin_0', 'bitcoin_3', 'bitcoin_4', 
#                 'hcv', 
#                 'random_4463_14',  'random_3155_31', 'random_943_41', 'random_3169_20', 'random_742_45', 'random_1382_42', 'random_814_46', 'random_760_45']
    

#     nums_to_categ_1 = [['label']] * 7 + [['category']] +  [randoms] * 8

#     # targets = ['label'] * 7  + ['category'] + ['target'] * 8

    

#     dropouts = ['marital_status', 'application_mode', 'application_order', 'course',
#        'daytime/evening_attendance', 'previous_qualification',
#        'previous_qualification_(grade)', 'nationality',
#        'mother\'s_qualification', 'father\'s_qualification',
#        'mother\'s_occupation', 'father\'s_occupation']

#     filenames_2 = ['autism','german','nursery','obesity','productivity_garment','Adult_v2',
#     'student-por','abalone','bank','bank-full','Adult_test_v2',
#     'Adult_train_v2','catheterization','coupons','default_credit',
#     'support2_3','taiwan_bankrupt_3','indian','recipes','support2_2',
#     'taiwan_bankrupt_2','catheterization_1','catheterization_2',
#     'catheterization_3','bank-full_2','Adult_v2_(bank-full)',
#     'bank-full_(Adult_v2)','drugs','egyptian','heart_failure','hepatitis',
#     'catheterization_21_2111','catheterization_21_3541',
#     'catheterization_21_4236','catheterization_21_5734',
#     'catheterization_29_2131','catheterization_29_3419',
#     'catheterization_29_4095','catheterization_29_5531',
#     'catheterization_38_584','catheterization_38_1399',
#     'catheterization_38_2074','catheterization_38_2284',
#     'catheterization_47_501','catheterization_47_1479',
#     'catheterization_47_2000','catheterization_47_2345',
#     'catheterization_55_553','catheterization_55_1599',
#     'catheterization_55_2122','catheterization_61_234',
#     'catheterization_61_521','catheterization_61_769',
#     'support2_16_9105',
#     'support2_26_1162','support2_26_2572','support2_26_3474',
#     'support2_32_1021','support2_32_1488','support2_32_2210',
#     'support2_36_1173','support2_36_1472','support2_36_2011',
#     'support2_46_509','support2_46_1045','support2_46_1510',
#     'support2_46_2131','support2_46_3419','support2_16_234',
#     'support2_16_521',
#     'support2_16_769',
#     'support2_26_553','support2_26_1599','support2_26_2122',
#     'support2_32_501','support2_32_1479','support2_32_2000',
#     'support2_32_2345','support2_36_584','support2_36_1399',
#     'support2_36_2074','support2_36_2284','support2_46_4095',
#     'support2_46_5531',
#     'dropout','dropout_15_1142','dropout_15_2510',
#     'dropout_15_3617','dropout_15_4424','dropout_20_1142','dropout_20_2510',
#     'dropout_20_3617','dropout_20_4424','dropout_25_1142','dropout_25_2510',
#     'dropout_25_3617','dropout_25_4424','dropout_30_2510','dropout_30_3617',
#     'dropout_30_4424','taiwan_16_1246','taiwan_16_2500','taiwan_16_3012',
#     'taiwan_16_4011','taiwan_26_743','taiwan_26_1272','taiwan_26_1999',
#     'taiwan_26_3256','taiwan_26_4011','taiwan_30_793','taiwan_30_1592',
#     'taiwan_30_2386','taiwan_30_3257','taiwan_51_1001','taiwan_51_1502',
#     'taiwan_61_721','taiwan_61_1001','taiwan_65_500','random_507_34',
#     'random_534_50','random_638_46','random_736_44','random_1711_27',
#     'random_1810_39','random_1969_46','random_2003_43','random_2031_49',
#     'random_2202_37','random_3109_30','random_1040_46','random_1071_41',
#     'random_1407_30','random_1560_48','random_1905_35','random_2016_38',
#     'random_2557_25','random_2705_33','random_2916_28','random_2998_14',
#     'random_4308_18','random_7711_5','random_536_41','random_724_50',
#     'random_800_43','random_867_50','random_1106_50','random_1270_47',
#     'random_1614_50','random_2044_47','random_2123_41','random_2142_38',
#     'random_764_50']

   
#     nums_to_categ_2 = [ 
#         None, None, ['class_encoded'], None, ['day', 'month'], None,
#          ['G1', 'G2'], None, ['day'], ['day'], None, 
#          None, None,  None,['education', 'marriage'], 
#         ['edu', 'prg6m', 'adlp'],   None , None , None, ['edu', 'prg6m', 'adlp'],
#        None, None, None,
#        None, ['day'], None,
#        ['day'], ['nicotine'], ['baseline_histological_grading','baseline_histological_staging'], None, None
#     ] +  [None] * 22 + [['edu', 'prg6m', 'adlp']] * 31 + [dropouts] * 16  + [None] * 18 + [randoms] * 34
    
#     filenames = filenames_1 + filenames_2
#     nums_to_categ = nums_to_categ_1 + nums_to_categ_2


#     return filenames, nums_to_categ #, targets

