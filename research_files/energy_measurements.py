from more_misc_functions import create_unique_folder
from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
import pyRAPL
from measurement_files.pet import *

def generate_synthetic_data_energy(exp_id, filename, epsilon, num_of_tuples, threshold):
    # original_stdout = sys.stdout
    # Redirect stdout to nowhere
    # sys.stdout = io.StringIO()
    pyRAPL.setup()
    measure = pyRAPL.Measurement('bar')
    measure.begin()
    input_data = '../preparation_files/datasets/' + filename + '.csv'
    represent_epsilon = str(epsilon)

    description_file = f'./output/{exp_id}/idea_description_{filename}_synthetic_data_{represent_epsilon}.json'
    synthetic_data = f'./output/{exp_id}/idea_{filename}_synthetic_data_{represent_epsilon}.csv'
    threshold_value = threshold

    degree_of_bayesian_network = 2

    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_correlated_attribute_mode(dataset_file=input_data, epsilon=epsilon, k=degree_of_bayesian_network)
    describer.save_dataset_description_to_file(description_file)

    # Generate data set
    generator = DataGenerator()
    generator.generate_dataset_in_correlated_attribute_mode(num_of_tuples, description_file)
    generator.save_synthetic_data(synthetic_data)
    measure.end()
    # sys.stdout = original_stdout
    pkg_energy = measure.result.pkg
    dram_energy = measure.result.dram
    energy = None
    
    if isinstance(pkg_energy, float) and isinstance(dram_energy, list):
        energy =  pkg_energy + sum(dram_energy)
    # Check if pkg_energy is a list and dram_energy is a float
    elif isinstance(pkg_energy, list) and isinstance(dram_energy, float):
        energy =  sum(pkg_energy) + dram_energy
    # Check if both are lists
    elif isinstance(pkg_energy, list) and isinstance(dram_energy, list):
        energy =  sum(pkg_energy) + sum(dram_energy)
    # Check if both are floats
    elif pkg_energy is None and dram_energy is None: return None
    elif pkg_energy is None:
        energy =  dram_energy
        if isinstance(energy, list):
            energy = sum(energy)
    elif dram_energy is None:
        energy =  pkg_energy
        if isinstance(energy, list):
            energy = sum(energy)
    # Check if both are floats
    else:
        energy =  pkg_energy + dram_energy
    
    # 1 Joule is 1,000,000 microJoules
    energy = energy / 1000000

    return energy


def profile_synthetic_data_generation_energy(filename, len_of_tuples, threshold):
    
    exp_id = create_unique_folder()
    epsilons = [0, 0.1]
    mems = []
    for epsilon in epsilons:
        res = generate_synthetic_data_energy(exp_id, filename, epsilon, len_of_tuples, threshold)
        mems.append(res)

    print(mems)
    return mems



def synthetic_data_generation(filename, len_of_tuples, threshold):
    
    exp_id = create_unique_folder()
    epsilons = [0, 0.1]
    mems = []
    for epsilon in epsilons:
        mems.append(lin_create_syn_data(exp_id, filename,  len_of_tuples, threshold ,epsilon))
        
    

    return mems