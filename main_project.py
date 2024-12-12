from framework_execution_files.prediction_files import *
from framework_execution_files.retrieve_data import *

"""

cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, cat_7, cat_8, cat_9, cat_10, cat_11, cat_12, cat_13, cat_14, cat_15, cat_16, cat_17, cat_18, cat_19, cat_20, cat_21, cat_22, cat_23, cat_24, cat_25, cat_26, cat_27, cat_28, cat_29, cat_30, cat_31, cat_32, cat_33, cat_34, cat_35, cat_36, cat_37, cat_38, cat_39, cat_40, cat_41, cat_42, cat_43, cat_44, cat_45, cat_46, cat_47, cat_48, cat_49, cat_50, cat_51
     


"""
def launch_estimation(filename = None, continuous_to_categorical = None, target = None, epsilon = None):
    # if filename is None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
    #     filename = input('Filename (exclude.csv):')
    # if continuous_to_categorical is None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty(): 
    #     continuous_to_categorical = input('Any continuous attributes that can be considered categorical? Write nothing if empty! (separate via comma)')
    #     continuous_to_categorical = continuous_to_categorical.split(',')
    #     continuous_to_categorical = [word.strip() for word in continuous_to_categorical]
    #     continuous_to_categorical = [item for item in continuous_to_categorical if item]
    #     if continuous_to_categorical == '':
    #         continuous_to_categorical = None
    
    # if target is None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
    #     target = input('What is the target attribute? (no extra spaces):').strip()
    # if epsilon is None and not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty(): 
    #     infff = input('With Differential Privacy (epsilon = 0.1) or without Differential Privacy (epsilon = 0)? Put 0 for no DP, otherwise put 1:')
    #     if infff == '1':
    #         epsilon = 0.1
    #     elif infff == '0':
    #         epsilon = 0
    #     else:
    #         print('Invalid input. Defaulting to epsilon = 0')
    #         epsilon = 0
     
    filename = 'random_2402_34'#'random_1091_50'
    continuous_to_categorical = [
    "cat_1", "cat_2", "cat_3", "cat_4", "cat_5", "cat_6", "cat_7", "cat_8", 
    "cat_9", "cat_10", "cat_11", "cat_12", "cat_13", "cat_14", "cat_15", 
    "cat_16", "cat_17", "cat_18", "cat_19", "cat_20", "cat_21", "cat_22", 
    "cat_23", "cat_24", "cat_25", "cat_26", "cat_27", "cat_28", "cat_29", 
    "cat_30", "cat_31", "cat_32", "cat_33", "cat_34", "cat_35", "cat_36", 
    "cat_37", "cat_38", "cat_39", "cat_40", "cat_41", "cat_42", "cat_43", 
    "cat_44", "cat_45", "cat_46", "cat_47", "cat_48", "cat_49", "cat_50", 
    "cat_51"
    ]
    target = 'target'

    epsilon = 0
    
    syn_records, else_records = retrieve_records()
    
    dataset_data = retrieve_dataset_data(filename, continuous_to_categorical, epsilon, target)
    
    energy_synthesis_prediction, energy_synthesis_accuracy = get_energy_synthesis_pred(syn_records, dataset_data, epsilon )
    singling_out_risk_prediction, singling_out_risk_accuracy =  get_singling_out_risk_pred(else_records, dataset_data, epsilon )
    # logres_energy_prediciton, logres_energy_accuracy = get_logres_energy_prediction(else_records, dataset_data, epsilon )
    logres_accuracy_prediciton, logres_accuracy_accuracy  = get_logres_accuracy_prediction(else_records, dataset_data, epsilon )
    # knn_energy_prediciton, knn_energy_accuracy = get_knn_energy_prediction(else_records, dataset_data, epsilon )
    knn_accuracy_prediciton, knn_accuracy_accuracy  = get_knn_accuracy_prediction(else_records, dataset_data, epsilon )
    results =  {
                        '1: Synthetic Data Generation Energy Consumption (Joules)': energy_synthesis_prediction, 
                        '1: Accuracy (R2 Score)': energy_synthesis_accuracy, 

                        '2: Singling Out Risk': singling_out_risk_prediction, 
                        '2: Accuracy (R2 Score)':  singling_out_risk_accuracy,


                        '3: Logistic Regression Accuracy': logres_accuracy_prediciton, 
                        '3: Accuracy (R2 Score)': logres_accuracy_accuracy,

                        '4: k-Nearest Neighbours Accuracy': knn_accuracy_prediciton,
                        '4: Accuracy (R2 Score)': knn_accuracy_accuracy
                        }
    
    
    print(f'For dataset {filename}')
    if epsilon == 0:
        print('Without Differential Privacy')
    else:
        print(f'With Differential Privacy (epsilon = {epsilon})')
    x = 0
    for i, k in results.items():
        if x % 2 == 0:
            print(f'{i} is {k}.')
        else:
            print(f'{i} is {k} (maximum is 1.0).')
        x += 1
        if x % 2 == 0:
            print('\n')
            x = 0










if __name__ == '__main__':
    launch_estimation()