import pandas as pd
from scipy.io import arff
import os
import numpy as np


def autism_clean():
    ...


    #Cleaning
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Autism Screening")

    arrf_file = arff.loadarff('Autism-Adult-Data.arff')
    # print(arrf_file)
    autism = pd.DataFrame(arrf_file[0])

    print(autism.head())
    autism = autism.rename(columns={"Class/ASD": "class", "jundice": "jaundice", "austim": "autism", "contry_of_res": "country"})
    print(autism.columns.tolist())
    print(autism.info())
    autism = autism.dropna()
    #We assume that 0 is no and 1 is yes
    autism = autism.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    print(autism.info())
    print(autism.head())
    #age_desc only has 1 unique record, meaning it's useless
    print(autism['age_desc'].unique())
    autism = autism.drop('age_desc', axis=1)
    print(autism.columns.tolist())
    autism = autism.applymap(lambda x: 1 if isinstance(x, str) and x.lower() == 'yes' else
                                  0 if isinstance(x, str) and x.lower() == 'no' else x)
    
    autism['age'] = autism['age'].astype('Int64')
    autism['result'] = autism['result'].astype('Int64')

    print(autism.head())

    '''
    A1 - A10: Answer to questions!
    
    '''

    
    os.chdir(owd)
    os.chdir("../preparation_files")
    
    # adult_train.to_c
    autism.to_csv('datasets/autism.csv', index=False)




if __name__ == '__main__':
    autism_clean()