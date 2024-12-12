import cProfile
import pstats
from memory_profiler import memory_usage
import pandas as pd
import numpy as np
import random
import os
from energy_measurements import *
from compute_characteristics import *
import sys
import io
from scipy.stats import entropy, skew, kurtosis
import statistics

from more_misc_functions import *
from measurement_files.check_privacy import *
from measurement_files.ml_tasks import *

from sklearn.model_selection import train_test_split

import traceback


        

def energy_measure(filenames, nums_to_categ):
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.max_rows', None)    
    pd.set_option('display.max_colwidth', None) 
    owd = os.getcwd()
    os.chdir(owd)
    
    
    dataset_info = {} 
    for i in range(len(filenames)):
        try:

            filename = filenames[i]
            num_to_categ = nums_to_categ[i]

            original_dataset = pd.read_csv('../preparation_files/datasets/' + filename + '.csv')
            dataset_memory_usage = original_dataset.memory_usage(deep=True).sum()
            memory_usage_mb = dataset_memory_usage / (1024 ** 2)

            em = []
            
            column_types = categorize_columns(original_dataset, num_to_categ)
        
            len_of_tuples, threshold = retrieve_values_for_pet(original_dataset, column_types)
            for i in range(3):
                mems = profile_synthetic_data_generation_energy(filename, len_of_tuples, threshold)
                em.append(mems)
            print(f'For {filename}')
            for mem in em:
                print(mem)
            epsilon_0 = []
            epsilon_1 = []
            for energy in em:
                epsilon_0.append(energy[0])
                epsilon_1.append(energy[1])
            energy = [statistics.median(epsilon_0), statistics.median(epsilon_1)]
            
            categorical_columns = {k: v for k, v in column_types.items() if v == 'Categorical'}
            sizes_of_categ = []
            for i in categorical_columns:
                sizes_of_categ.append(original_dataset[i].nunique())
            sizes_of_categ = np.array(sizes_of_categ)
            continuous_columns = [k for k, v in column_types.items() if v == 'continuous']
            complexity_metrics, distribution_metrics, mean_std_dev,  mean_variance,max_std_dev, max_variance,mean_continuous_correlation, max_continuous_correlation = compute_dist_compl(original_dataset, categorical_columns, continuous_columns)

            
            dataset_info[filename] = {
                'size_mb': memory_usage_mb,
                'num_records': original_dataset.shape[0],
                'num_attributes': original_dataset.shape[1],
                'num_categorical_attributes': len(categorical_columns),
                'num_continuous_attributes': original_dataset.shape[1] - len(categorical_columns),
                'max_categorical_unique': threshold - 1,
                'min_categorical_unique': np.min(sizes_of_categ),
                'mean_categorical_unique': np.mean(sizes_of_categ),
                'complexity_metrics': complexity_metrics,
                'distribution_metrics': distribution_metrics,
                'mean_std_dev': mean_std_dev,
                'mean_variance': mean_variance,
                'mean_continuous_correlation': mean_continuous_correlation,
                'max_continuous_correlation': max_continuous_correlation,
                'max_std_dev': max_std_dev,
                'max_variance': max_variance,
                'energy_measurements': energy
            }
            print(dataset_info[filename])
        except Exception as e:
            print(f'Something went wrong with {filename}. Error: {e}')



        records = []
        for dataset_name, info in dataset_info.items():
            epsilon = 0
            energy = info['energy_measurements'][0]
            print(f'Hello epsi: {epsilon} and energy {energy}')
            record = {
                'dataset_name': dataset_name,
                'epsilon': epsilon,
                'size_mb': info['size_mb'],
                'num_records': info['num_records'],
                'num_attributes': info['num_attributes'],
                'num_categorical_attributes': info['num_categorical_attributes'],
                'num_continuous_attributes': info['num_continuous_attributes'],
                'max_categorical_unique': info['max_categorical_unique'],
                'min_categorical_unique': info['min_categorical_unique'],
                'mean_categorical_unique': info['mean_categorical_unique'],
                'entropy': info['complexity_metrics'],
                'skewness': info['distribution_metrics']['skewness'],
                'kurtosis': info['distribution_metrics']['kurtosis'],
                'mean_std_dev': info['mean_std_dev'],
                'mean_variance': info['mean_variance'],
                'mean_continuous_correlation': info['mean_continuous_correlation'],
                'max_continuous_correlation': info['max_continuous_correlation'],
                'max_std_dev': info['max_std_dev'],
                'max_variance': info['max_variance'],
                'energy': energy
            }
            records.append(record)
            print(record)
            epsilon = 0.1
            energy = info['energy_measurements'][1]
            print(f'Hello epsi: {epsilon} and energy {energy}')
            record = {
                'dataset_name': dataset_name,
                'epsilon': epsilon,
                'size_mb': info['size_mb'],
                'num_records': info['num_records'],
                'num_attributes': info['num_attributes'],
                'num_categorical_attributes': info['num_categorical_attributes'],
                'num_continuous_attributes': info['num_continuous_attributes'],
                'max_categorical_unique': info['max_categorical_unique'],
                'min_categorical_unique': info['min_categorical_unique'],
                'mean_categorical_unique': info['mean_categorical_unique'],
                'entropy': info['complexity_metrics'],
                'skewness': info['distribution_metrics']['skewness'],
                'kurtosis': info['distribution_metrics']['kurtosis'],
                'mean_std_dev': info['mean_std_dev'],
                'mean_variance': info['mean_variance'],
                'mean_continuous_correlation': info['mean_continuous_correlation'],
                'max_continuous_correlation': info['max_continuous_correlation'],
                'max_std_dev': info['max_std_dev'],
                'max_variance': info['max_variance'],
                'energy': energy
            }
            records.append(record)
            print(record)
        
    df = pd.DataFrame(records)
    df.to_csv('energy_records.csv', index=False) 
    print("Saved as 'energy_records.csv' ")


def measure_the_rest(filenames, nums_to_categ, targets, linkability_sets, secret):
 
    
    # owd = os.getcwd()
    # os.chdir(owd)
   

    dataset_info = {} 
    for i in range(len(filenames)):
        try:

            filename = filenames[i]
            num_to_categ = nums_to_categ[i]

            target = targets[i]

            original_dataset = pd.read_csv('datasets/' + filename + '.csv')
            dataset_memory_usage = original_dataset.memory_usage(deep=True).sum()
            memory_usage_mb = dataset_memory_usage / (1024 ** 2)
            if len(linkability_sets) == 0:
                our_list = original_dataset.columns.tolist()
                small = len(our_list)
                linkability_set = []
                exclude = []
                for i in range(0, 2):
                    subset = []
                    for j in range(0,3):
                        num = random.randint(0, small -1)
                        while num in exclude:
                            num = random.randint(0, small-1)
                        subset.append(our_list[num])
                    linkability_set.append(subset)
                    

            else:
                if linkability_sets[i] ==0:
                    our_list = original_dataset.columns.tolist()
                    small = len(our_list)
                    linkability_set = []
                    exclude = []
                    for i in range(0, 2):
                        
                        subset = []
                        for j in range(0,3):
                            num = random.randint(0, small-1)
                            while num in exclude:
                                num = random.randint(0, small-1)
                            subset.append(our_list[num])
                        linkability_set.append(subset)
                else:
                    linkability_set = linkability_sets[i]
            
            column_types = categorize_columns(original_dataset, num_to_categ)
        
            len_of_tuples, threshold = retrieve_values_for_pet(original_dataset, column_types)
            
            all_syn_data_info = synthetic_data_generation(filename, len_of_tuples, threshold)
            risks = []
        
            energy_knn = []
            accuracies_knn = []
            k_values = []
            energy_logres = []
            accuracies_logres = []
            for syn_data_info in all_syn_data_info:
                syn_df = pd.read_csv(syn_data_info[1])
                train_syn_with_target, test_syn_with_target = train_test_split(syn_df, test_size=0.2, random_state=42)
            
                syn_data_train, syn_target_train, syn_data_test, syn_target_test = prep_for_ml(syn_df, target, column_types) 
                syn_privacy_risks = 0
                print("\nEvaluating Risks!")
                attack_num = 5
                while syn_privacy_risks == 0:
                    try:
                        num_of_attacks = round(len(test_syn_with_target) / attack_num)
                        syn_privacy_risks = check_privacy_risks(original_dataset, train_syn_with_target, test_syn_with_target, linkability_set, secret, num_of_attacks)
                        break
                    except RuntimeError:
                        attack_num += 1

                risks.append(syn_privacy_risks)
                results_knn  = knn_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
                accuracies_knn.append(results_knn['Accuracy'])
                k_values.append(results_knn['K-value'])
                energy_knn.append(results_knn['Energy'])
                results_logres = logres_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test)
                accuracies_logres.append(results_logres['Accuracy']) 
                energy_logres.append(results_logres['Energy'])       





            print(f'Results for {filename} are added')
        
            
            categorical_columns = {k: v for k, v in column_types.items() if v == 'Categorical'}
            sizes_of_categ = []
            for x in categorical_columns:
                sizes_of_categ.append(original_dataset[x].nunique())
            sizes_of_categ = np.array(sizes_of_categ)
            continuous_columns = [k for k, v in column_types.items() if v == 'continuous']
            complexity_metrics, distribution_metrics, mean_std_dev,  mean_variance,max_std_dev, max_variance,mean_continuous_correlation, max_continuous_correlation = compute_dist_compl(original_dataset, categorical_columns, continuous_columns)

            
            dataset_info[filename] = {
                'size_mb': memory_usage_mb,
                'num_records': original_dataset.shape[0],
                'num_attributes': original_dataset.shape[1],
                'num_categorical_attributes': len(categorical_columns),
                'num_continuous_attributes': original_dataset.shape[1] - len(categorical_columns),
                'max_categorical_unique': threshold - 1,
                'min_categorical_unique': np.min(sizes_of_categ),
                'mean_categorical_unique': np.mean(sizes_of_categ),
                'complexity_metrics': complexity_metrics,
                'distribution_metrics': distribution_metrics,
                'mean_std_dev': mean_std_dev,
                'mean_variance': mean_variance,
                'mean_continuous_correlation': mean_continuous_correlation,
                'max_continuous_correlation': max_continuous_correlation,
                'max_std_dev': max_std_dev,
                'max_variance': max_variance,
                'privacy_risks': risks,
                # 'energy_knn': energy_knn,
                'accuracy_knn': accuracies_knn,
                'k-values': k_values,
                # 'energy_logres': energy_logres,
                'accuracy_logres': accuracies_logres
            }
            print(dataset_info[filename])
        except Exception as e:
            print(f'Something went wrong with {filename}. Error: {e}')

    return dataset_info
     

def result_sort(dataset_info):
    records = []
    print('Sorting out all results!')


    for dataset_name, info in dataset_info.items():
        # Iterate twice for each epsilon value
        for epsilon_index, epsilon in enumerate([0, 0.1]):
            record = {
                'dataset_name': dataset_name,
                'epsilon': epsilon,
                'size_mb': info['size_mb'],
                'num_records': info['num_records'],
                'num_attributes': info['num_attributes'],
                'num_categorical_attributes': info['num_categorical_attributes'],
                'num_continuous_attributes': info['num_continuous_attributes'],
                'max_categorical_unique': info['max_categorical_unique'],
                'min_categorical_unique': info['min_categorical_unique'],
                'mean_categorical_unique': info['mean_categorical_unique'],
                'entropy': info['complexity_metrics'],
                'skewness': info['distribution_metrics']['skewness'],
                'kurtosis': info['distribution_metrics']['kurtosis'],
                'mean_std_dev': info['mean_std_dev'],
                'mean_variance': info['mean_variance'],
                'mean_continuous_correlation': info['mean_continuous_correlation'],
                'max_continuous_correlation': info['max_continuous_correlation'],
                'max_std_dev': info['max_std_dev'],
                'max_variance': info['max_variance'],
                'singling_out_risk': info['privacy_risks'][epsilon_index]['Singling Out'],
                # 'linkability_risk': info['privacy_risks'][epsilon_index]['Linkability'],
                # 'inference_risk': info['privacy_risks'][epsilon_index]['Inference'],
                # 'energy_knn': info['energy_knn'][epsilon_index],
                'accuracy_knn': info['accuracy_knn'][epsilon_index],
                'k-values': info['k-values'][epsilon_index],
                # 'energy_logres': info['energy_logres'][epsilon_index],
                'accuracy_logres': info['accuracy_logres'][epsilon_index]
            }
            records.append(record)


    df = pd.DataFrame(records)

    df.to_csv('privacy_utility_records.csv', index=False)
    print("Data has been sorted and saved to 'privacy_utility_records.csv'.")


if __name__ == "__main__":

    filenames, numerical_to_categorical, targets = data_preparation_for_data_collection()
    energy_measure(filenames, numerical_to_categorical)
    dataset_info = measure_the_rest(filenames, numerical_to_categorical, targets, [], 'secret')
    result_sort(dataset_info)
    achieve_more_data(filenames, numerical_to_categorical, targets)




    
    


