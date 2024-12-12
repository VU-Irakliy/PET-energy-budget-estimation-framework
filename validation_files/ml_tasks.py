from codecarbon import track_emissions
from codecarbon import EmissionsTracker
import pyRAPL
import pandas as pd
from validation_files.misc_functions import tracker_launcher
import sys
import io

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from math import sqrt
from collections import defaultdict

"""
2 functions for linux
2 functions for other OS
1 for separating the datasets
"""
import warnings

from sklearn.model_selection import train_test_split

def knn_misc(syn_data_train, syn_target_train, syn_data_test, syn_target_test):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    k_value = round((sqrt(len(syn_data_train)))/ 2)
    
    # original_stdout = sys.stdout
    # # Redirect stdout to nowhere
    # sys.stdout = io.StringIO()

    # tracker = tracker_launcher()
    
    # tracker.start()

    
    NeighbourModel = KNeighborsClassifier(n_neighbors=k_value)
    NeighbourModel.fit(syn_data_train, syn_target_train.values.ravel())

    
    # tracker.stop()
    #1 kilowatt-hour (kWh) is equal to 3,600,000 joules (J).
    # result_energy = tracker._total_energy.kWh * 3600000

    report = classification_report(syn_target_test, NeighbourModel.predict(syn_data_test), output_dict=True)

    accuracy = report['accuracy']

    # exit()
    results = {
        'Accuracy': accuracy,
        'K-value' : k_value
        # ,
        # 'Energy':result_energy
    }
   

    # sys.stdout = original_stdout
    return results

    #acquire accuracy, k value, and energy consumption

    



def logres_misc(syn_data_train, syn_target_train, syn_data_test, syn_target_test):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    # original_stdout = sys.stdout
    # # Redirect stdout to nowhere
    # sys.stdout = io.StringIO()


    # tracker = tracker_launcher()
    
    # tracker.start()
    

    # make Logistics Regression model
    LogReg = LogisticRegression(max_iter=1000)
    LogReg.fit(syn_data_train, syn_target_train.values.ravel())

    # tracker.stop()
    #1 kilowatt-hour (kWh) is equal to 3,600,000 joules (J).
    # result_energy = tracker._total_energy.kWh * 3600000


    # predict and print report
    predictions = LogReg.predict(syn_data_test)
    report = classification_report(syn_target_test.values.ravel(), predictions, output_dict=True)
    # print(f"The accuracy for the adult data set is: {report['accuracy']}")

    # save results to csv
    accuracy = report['accuracy']

    results = {
        'Accuracy': accuracy
        # ,
        # 'Energy':result_energy 
    }
    return results
    # sys.stdout = original_stdout


    




"""



LINUX



"""
def knn_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test):
    
    k_value = round((sqrt(len(syn_data_train)))/ 2)
    
    # pyRAPL.setup()
    # measure = pyRAPL.Measurement('bar')
    # measure.begin()

    NeighbourModel = KNeighborsClassifier(n_neighbors=k_value)
    NeighbourModel.fit(syn_data_train, syn_target_train.values.ravel())


    # measure.end()
    report = classification_report(syn_target_test, NeighbourModel.predict(syn_data_test), output_dict=True)

    accuracy = report['accuracy']


    # pkg_energy = measure.result.pkg
    # dram_energy = measure.result.dram

    # energy = None
    # # print(pkg_energy, dram_energy)
    # if isinstance(pkg_energy, float) and isinstance(dram_energy, list):
    #     energy =  pkg_energy + sum(dram_energy)
    # # Check if pkg_energy is a list and dram_energy is a float
    # elif isinstance(pkg_energy, list) and isinstance(dram_energy, float):
    #     energy =  sum(pkg_energy) + dram_energy
    # # Check if both are lists
    # elif isinstance(pkg_energy, list) and isinstance(dram_energy, list):
    #     energy =  sum(pkg_energy) + sum(dram_energy)
    # elif pkg_energy is None and dram_energy is None: 
    #     print('Error with energy measurements. Value is now 0.')
    #     energy = 0
    # elif isinstance(pkg_energy, None):
    #     energy =  dram_energy
    # elif isinstance(dram_energy, None):
    #     energy =  dram_energy
    # # Check if both are floats
    # else:
    #     energy =  pkg_energy + dram_energy
    
    # # 1 Joule is 1,000,000 microJoules
    # energy = energy / 1000000

    # exit()
    results = {
        'Accuracy': accuracy,
        'K-value' : k_value
        # ,
        # 'Energy': energy
    }
    return results

    



def logres_lin(syn_data_train, syn_target_train, syn_data_test, syn_target_test):
    pyRAPL.setup()
    measure = pyRAPL.Measurement('bar')
    measure.begin()

    
    LogReg = LogisticRegression(max_iter=1000)
    LogReg.fit(syn_data_train, syn_target_train.values.ravel())

    measure.end()
    
    predictions = LogReg.predict(syn_data_test)
    report = classification_report(syn_target_test.values.ravel(), predictions, output_dict=True)

    accuracy = report['accuracy']

    pkg_energy = measure.result.pkg
    dram_energy = measure.result.dram
    energy = None
    # Check if pkg_energy is a float and dram_energy is a list
    if isinstance(pkg_energy, float) and isinstance(dram_energy, list):
        energy =  pkg_energy + sum(dram_energy)
    # Check if pkg_energy is a list and dram_energy is a float
    elif isinstance(pkg_energy, list) and isinstance(dram_energy, float):
        energy = sum(pkg_energy) + dram_energy
    # Check if both are lists
    elif isinstance(pkg_energy, list) and isinstance(dram_energy, list):
        energy =  sum(pkg_energy) + sum(dram_energy)
    elif pkg_energy is None and dram_energy is None: 
        print('Error with energy measurements. Value is now 0.')
        energy = 0
    elif isinstance(pkg_energy, None):
        energy =  dram_energy
    elif isinstance(dram_energy, None):
        energy =  dram_energy
    # Check if both are floats
    else:
        energy =  pkg_energy + dram_energy
    
    # 1 Joule is 1,000,000 microJoules
    energy = energy / 1000000

    

    results = {
        'Accuracy': accuracy,
        'Energy':energy 
    }
    return results
    
"""



PREPARING DATASETS FOR ML TASKS



"""


def prep_for_ml(df, target, column_types):

    # train_syn_for_privacy, test_syn_for_privacy = split_datasets(exp_id, syn_data_file)
    

    df2 = df.copy()

    info_sort = column_types.copy()
    info_sort[target] = None

    categorical_columns = [k for k, v in info_sort.items() if v == 'Categorical']
    continuous_columns = [k for k, v in info_sort.items() if v == 'continuous']


   
    # Use MinMax scaler for continuous/continuous features
    df2[continuous_columns] = MinMaxScaler().fit_transform(df2[continuous_columns])

    # Use One-hot encoding for categorical features
    df2 = pd.get_dummies(df2,columns = categorical_columns)

    train_ml_dataset, test_ml_dataset = train_test_split(df2, test_size=0.2, random_state=42)

    isolated_column_train = train_ml_dataset[[target]]

    remaining_columns_train = train_ml_dataset.drop(columns=[target])

    isolated_column_test = test_ml_dataset[[target]]

    remaining_columns_test = test_ml_dataset.drop(columns=[target])

    # isolated_column_test = test_df[[target]]

    # remaining_columns_test = test_df.drop(columns=[target])
    # remaining_columns_test[continuous_columns] = MinMaxScaler().fit_transform(remaining_columns_test[continuous_columns])
    # remaining_columns_test = pd.get_dummies(remaining_columns_test,columns = categorical_columns)
    # print(remaining_columns_train.head())
    # print(remaining_columns_test.head())

    return  remaining_columns_train, isolated_column_train, remaining_columns_test, isolated_column_test