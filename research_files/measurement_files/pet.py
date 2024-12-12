from codecarbon import track_emissions
from codecarbon import EmissionsTracker
import pyRAPL
import pandas as pd
from measurement_files.misc_functions import tracker_launcher, is_it_a_list
from termcolor import colored


from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator


def lin_create_syn_data(exp_id, input_filename, num_of_tuples, threshold, input_epsilon):
    print("\n")
    represent_epsilon = str(input_epsilon)
    print("Epsilon value is " + colored(f'{str(input_epsilon)}', 'green') + '.')
    if input_epsilon == 0.1:
        represent_epsilon = represent_epsilon.replace(".", ",")
  
    print("Synthetic Data generation has started. Please wait...\n")


    
    input_data = 'datasets/'+ input_filename + '.csv'

    # location of two output files
    mode = 'correlated_attribute_mode'
    description_file = f'./output/' + str(exp_id) +'/description_'+ input_filename +  '_synthetic_data'+ '_' + represent_epsilon + '.json'
    synthetic_data = f'./output/' + str(exp_id) + '/'+ input_filename  + '_synthetic_data'+ '_' + represent_epsilon +'.csv'
    
    """
    https://github.com/MarcDane/PETs_Energy-Utility-Risks/blob/master/03-dataset_generation.py   Why all categorical? This doesn't make sense!
    
    """
    
    #An attribute is categorical if its domain size is less than this threshold.
    # Here modify the threshold to adapt to the domain size of "education" (which is 14 in input dataset).
    threshold_value = threshold

    # A parameter in Differential Privacy. It roughly means that removing a row in the input dataset will not 
    # change the probability of getting the same output more than a multiplicative difference of exp(epsilon).
    # Increase epsilon value to reduce the injected noises. Set epsilon=0 to turn off differential privacy.
    epsilon = input_epsilon

    # The maximum number of parents in Bayesian network, i.e., the maximum number of incoming edges.
    degree_of_bayesian_network = 2

    # Number of tuples generated in synthetic dataset. (just add the number of the rows that exist automatically)
    num_tuples_to_generate = num_of_tuples # Here 32561 is the same as input dataset, but it can be set to another number.
    
    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_correlated_attribute_mode(dataset_file=input_data, 
                                                            epsilon=epsilon, 
                                                            k=degree_of_bayesian_network)
    describer.save_dataset_description_to_file(description_file)

    # Generate data set
    generator = DataGenerator()
    generator.generate_dataset_in_correlated_attribute_mode(num_tuples_to_generate, description_file)
    generator.save_synthetic_data(synthetic_data)

   


    return [description_file, synthetic_data]
