from anonymeter.evaluators import SinglingOutEvaluator
from anonymeter.evaluators import LinkabilityEvaluator
from anonymeter.evaluators import InferenceEvaluator
import os
import statistics
from collections import defaultdict
from termcolor import colored
import warnings

def check_privacy_risks(original_dataset, train_syn_with_target, test_syn_with_target, known_attribute_distributions, input_secret, num_of_attacks): 
                                                                                                                                                #1 if List, 0 if List of lists

    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    #For Inference Risk
    
    aux_list_2 = known_attribute_distributions[0]
    
    


    print('Singling Out risk measurement...')
    evaluatorSinglingOut = SinglingOutEvaluator(ori= original_dataset,
                       syn= train_syn_with_target,
                       control= test_syn_with_target,
                       n_attacks= num_of_attacks)

    evaluatorSinglingOut.evaluate(mode='univariate')
    riskSingle = evaluatorSinglingOut.risk().value
    print("\n")

    # print('Linkability risk measurement...')
    # print(f"Features of the records that are given to the attacker as auxiliary information: {known_attribute_distributions} ")
    # # print("Note:")
    # # print(colored("If you see \"UserWarning: Attack is as good or worse as baseline model.\", it means that provided attributes cannot be used to link to the dataset. Too random or little info", "blue"))
    # # print(colored("Therefore, it's necessary to provide better attributes or adding attributes to second dataset for truly testing the security of the produced dataset.\n", "blue"))
    
    # evaluatorLinkability = LinkabilityEvaluator(ori= original_dataset,
    #                    syn= train_syn_with_target,
    #                    control= test_syn_with_target,
    #                    n_attacks= num_of_attacks,
    #                    aux_cols = known_attribute_distributions
    #                    )
    

    # evaluatorLinkability.evaluate(n_jobs=-2)
    # riskLinkability = evaluatorLinkability.risk().value
    
    # print('\nInference risk measurement...')
    # riskInference = None
    # if input_secret == None:
    #     #loop, so each one attribute could be considered a known attribute
    #     print(f"Features of the records that are given to the attacker as auxiliary information: {aux_list_2} (we only consider the first dataset if 2 were provided)")
    #     potential_secrets = original_dataset.columns.difference(aux_list_2).tolist()
    #     print(f"Each attribute here will be treated as a secret to calculate mean Inference risk: {potential_secrets}")
    #     inf_risk_results = []
    #     for secret in potential_secrets:
    #         evaluatorInference = InferenceEvaluator(ori= original_dataset,
    #                     syn= train_syn_with_target,
    #                     control= test_syn_with_target,
    #                     n_attacks= num_of_attacks,
    #                     aux_cols = aux_list_2,
    #                     secret = secret)

    #         evaluatorInference.evaluate(n_jobs=-2)
    #         i_inf_risk = evaluatorInference.risk().value
    #         inf_risk_results.append(i_inf_risk)
        
    #     riskInference = statistics.mean(inf_risk_results)
        
    # else:
    #     print("Our secret: " + input_secret)
    #     print(f"Features of the records that are given to the attacker as auxiliary information: {aux_list_2} (we only consider the first dataset if 2 were provided)")
    #     evaluatorInference = InferenceEvaluator(ori= original_dataset,
    #                     syn= train_syn_with_target,
    #                     control= test_syn_with_target,
    #                     n_attacks= num_of_attacks,
    #                     aux_cols = aux_list_2,
    #                     secret = input_secret)

    #     evaluatorInference.evaluate(n_jobs=-2)
    #     riskInference = evaluatorInference.risk().value
   
    results = {
        "Singling Out": riskSingle
        # ,
        # "Linkability": riskLinkability,
        # "Inference" :riskInference,

    }
    return results
