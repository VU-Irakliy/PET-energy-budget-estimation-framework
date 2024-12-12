
import random
import pandas as pd
import os
from collections import defaultdict
import sys

from single_measurement_files.misc_functions import *
from single_measurement_files import pet
from single_measurement_files import ml_tasks
from single_measurement_files import check_privacy
import time


from termcolor import colored

                                                                                                    #op_sys: 0 is misc, 1 is linux
def main_framework(input_filename, target_attribute_ML, num_to_categ,  input_possible_known_attributes, input_secret, op_sys):
    
    if not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
        preprocess = input("Were your datasets cleaned, preprocessed and saved in .CSV? Answer Y or N :")
        print('\n')
        if preprocess.replace(" ", "").upper() != "Y":
            print("Please preprocess the dataset before the execution of the framework (without MinMaxScaler and One-Hot encoding!).")
            print('Make sure that this process doesn\'t alter the data itself!')
            print("This can affect the quality of the results['results'].")
            exit()
        
    print(colored("Reminder: Please clean and preprocess the dataset before the execution of the framework (without MinMaxScaler and One-Hot encoding!).", 'yellow'))
    print('Data must not be altered!')
    
   
    filename, target, continuous_to_categorical, possible_columns, secret = organise_all_input(input_filename, target_attribute_ML, num_to_categ, input_possible_known_attributes, input_secret)

    original_dataset = pd.read_csv('put_your_dataset_here/'+ filename + '.csv')
    

    what_kind_of_list = determine_the_list(possible_columns, original_dataset, secret)  #1 if List, 0 if List of lists

    column_types = categorize_columns(original_dataset, continuous_to_categorical)
    
    #Demonstrate, what attributes are which type.
    categorical_columns = [k for k, v in column_types.items() if v == 'Categorical']
    continuous_columns = [k for k, v in column_types.items() if v == 'continuous']
    # print(colored('Don\'t forget to check the accuracy of the properties of each attribute! You will have 5 seconds', 'yellow'))
    print(f'Categorical attributes: {categorical_columns}')
    print(f'Continuous attributes: {continuous_columns} \n')
    print('Please check the data type of attributes. Stop the process if necessary.')
    
    epsilon_values = [0, 0.1]
    
    #Creating a unique folder for our output, so the user could find the results['results']!
    exp_id = create_unique_folder()
    print("Iteration's ID is: " + str(exp_id) + " !\n")

    results= defaultdict(dict)
    results['results'] = defaultdict(dict)
    results['ID'] = exp_id
    results['input'] = {
        'Filename': filename,
        'Target': target,
        'Possible known attributes': possible_columns,
        'Secret attribute': secret,
        'Categorical attributes': categorical_columns,
        'Continuous attributes': continuous_columns,
        'Number of records': original_dataset.shape[0],
        'Number of attributes': original_dataset.shape[1]
    }
    

    num_of_tuples, threshold = retrieve_values_for_pet(original_dataset, column_types)
    
    if num_of_tuples == False:
        exit()
    
    ####EXPERIMENT ITSELF
    for eps in epsilon_values:
        if op_sys == 0:
            syn_energy, syn_description, syn_data_file = pet.misc_create_syn_data(exp_id, filename, num_of_tuples, threshold, eps)
            os.remove("emissions.csv")
        else:
            syn_energy, syn_description, syn_data_file = pet.lin_create_syn_data(exp_id, filename, num_of_tuples, threshold, eps)



        results['results'][f'syn_data_{eps}']['epsilon'] = eps
        results['results'][f'syn_data_{eps}']["energy_synthesis"] = syn_energy
        print('Files that will be used for risk analysis and ML tasks.')
        print(syn_description, syn_data_file)
        
        
        #Now, we need to split the dataset into 2: train and test.
        syn_df = pd.read_csv(syn_data_file)
        train_syn_with_target, test_syn_with_target = train_test_split(syn_df, test_size=0.2, random_state=42)
        
        syn_data_train, syn_target_train, syn_data_test, syn_target_test = ml_tasks.prep_for_ml(syn_df, target, column_types) 
        
        print("\nEvaluating Risks!")
        num_of_attacks = round(len(test_syn_with_target) / 5)
        syn_privacy_risks = check_privacy.check_privacy_risks(original_dataset, train_syn_with_target, test_syn_with_target, possible_columns, secret, num_of_attacks, what_kind_of_list)
        results['results'][f'syn_data_{eps}']["risks"] = syn_privacy_risks
        
        #Preprocessing datasets for ML tasks
        
        if op_sys == 0:
            print('\nEvaluating accuracy with K-nearest neighbors...')
            results['results'][f'syn_data_{eps}']['knn'] = ml_tasks.knn_misc(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
            results['results'][f'syn_data_{eps}']['knn']['Total energy'] = float(syn_energy) + float(results['results'][f'syn_data_{eps}']['knn']['Energy'])
            print('\nEvaluating accuracy with Logistic Regression...')
            results['results'][f'syn_data_{eps}']['logres'] = ml_tasks.logres_misc(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
            results['results'][f'syn_data_{eps}']['logres']['Total energy'] = float(syn_energy) + float(results['results'][f'syn_data_{eps}']['logres']['Energy'])
            # print(results['results'][f'syn_data_{eps}']['logres']['Total energy'])
            os.remove("emissions.csv")
        else:
            print('\nEvaluating accuracy with K-nearest neighbors...')
            results['results'][f'syn_data_{eps}']['knn'] = ml_tasks.knn_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
            results['results'][f'syn_data_{eps}']['knn']['Total energy'] = float(syn_energy) + float(results['results'][f'syn_data_{eps}']['knn']['Energy'])
            print('\nEvaluating accuracy with Logistic Regression...')
            results['results'][f'syn_data_{eps}']['logres'] = ml_tasks.logres_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
            results['results'][f'syn_data_{eps}']['logres']['Total energy'] = float(syn_energy) + float(results['results'][f'syn_data_{eps}']['logres']['Energy'])

    print('\n')



    return results

    




"""
###########################################################################################################################
ORGANISING ALL OF THE INPUT
###########################################################################################################################

"""



def organise_all_input(input_filename, target_attribute_ML, num_to_categ,  input_possible_known_attributes, input_secret):
    filename = None
 
    if input_filename != None:
        filename = input_filename
    else:
        filename = str(input("Enter a file name (exclude .csv): "))
        # filename = 'Adult_v2'
    
    print("You have a single file!\n")
    
    ###########################################################################################################
    target = None
    
    if target_attribute_ML != None:
        target = target_attribute_ML
    else:
        target = str(input("What is a target column for ML tasks? Avoid unnecessary spaces: "))
        target.strip()
        # target = "income"


    continuous_to_categorical = None
    if num_to_categ == None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
        #what num attributes can be considered as categorical?
        print("\nAny continuous attributes that can be considered categorical?")
        continuous_to_categorical = input("Leave empty if none. Otherwise, write down those features with comma as a separator: ")
        continuous_to_categorical = continuous_to_categorical.split(',')
        continuous_to_categorical = [word.strip() for word in continuous_to_categorical]
        continuous_to_categorical = [item for item in continuous_to_categorical if item]
        if continuous_to_categorical == '':
            continuous_to_categorical = None
    else:
        continuous_to_categorical = num_to_categ
    
    ###########################################################################################################    
    # secret = None
    # if input_secret == None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
    #     print("\nProvide the secret column for attacker to guess? (for Inference risk measurement) Check for grammar!")
    #     print(colored("It's optional. Meaning if left empty,", "yellow") + colored(" the framework will work much longer (depending on number of attributes) ", "red") + colored("and will calculate average Inference risk.", "yellow"))
    #     secret = input("Secret: ")
    #     print('\n')
    #     secret = secret.strip()
    #     if secret == "":
    #         secret = None

    # else:
    #     secret = input_secret

    # ###########################################################################################################
    # possible_columns = None
    # if input_possible_known_attributes == None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
    #     ...
    #     print("\nWhich attributes could be known to the attacker? Required for risk evaluations." )
    #     print("Which is why we need you to provide attributes from your datasets for 2 hypothetical datasets that attacker has access to.")
    #     print("First one will be used for both Linkability and Inference risk measurements.")
    #     print("Second one is recommended and will be used only for Linkability risk measurement.")
    #     print(colored("Use comma to separate attributes!!!!!! And check grammar as it can affect the results.", "yellow"))
    #     print(colored("Make sure there are no duplicates!", "yellow"))
    #     print(colored("Exclude the secret attribute (if there is one) from these datasets.", "yellow"))
    #     attr_inputs = input("First dataset: ")
    #     if len(attr_inputs) == 0:
    #         print("You have provided no input")
    #         exit()
    #     attr_inputs_2 = input("Second dataset for Linkability risk measurement: ")

        


    #     possible_col = attr_inputs.split(',')

    #     # # Strip any leading/trailing whitespace from each word
    #     possible_columns = [word.strip() for word in possible_col]
    #     possible_columns = [item for item in possible_columns if item]
    #     if secret != None and secret in possible_columns:
    #         possible_columns.remove(secret)

    #     if len(attr_inputs_2) != 0:
    #         possible_col_2 = attr_inputs_2.split(',')

    #         # Strip any leading/trailing whitespace from each word
    #         possible_columns_2 = [word.strip() for word in possible_col_2]
    #         if secret in possible_columns_2 and secret != None:
    #                 possible_columns_2.remove(secret)
    #         if len(possible_columns_2) != 0 and possible_columns_2 != ['']:
    #             possible_columns = [possible_columns, possible_columns_2]

                
            
        

    # elif input_possible_known_attributes != None:
    #     possible_columns = input_possible_known_attributes
    # #remove a secret, if it somehow ended up in the lists
    #     if secret != None:
    #         if is_it_a_list(possible_columns) == 2:
    #             for i in possible_columns:
    #                 if secret in i:
    #                     i.remove(secret)
    #         elif is_it_a_list(possible_columns) == 1:
    #             if secret in possible_columns:
    #                 possible_columns.remove(secret)
    #         else:
    #             print("Something wrong with the list. Exiting the program.")
    #             exit()
    # else:
    #     print("No input provided for auxiliary attributes. Exiting the program.")
    #     exit()
    



    
    return filename, target, continuous_to_categorical, #possible_columns, secret


