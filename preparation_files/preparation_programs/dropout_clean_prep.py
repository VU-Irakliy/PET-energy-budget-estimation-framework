
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder




"""
10-11          0-9
(sufficient)   (fail)
D                 F
(from the paper Cortez, P. and A. M. Gonçalves Silva. “Using data mining to predict secondary school student performance.” (2008).)

Therefore, minimum passing grade is 10!

"""

def clean_dropout():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Dropout")
    student = pd.read_csv('data.csv', sep=';')
    
    print(student.head())
    print(student['Target'].unique())
    le = LabelEncoder()

    # Fit and transform the 'class' column
    student['Target'] = le.fit_transform( student['Target'])
    print(student['Target'].unique())
    student.columns = student.columns.str.lower().str.replace(' ', '_')
    
    student = student.rename(columns={
        'daytime/evening_attendance\t': 'daytime/evening_attendance',
        'nacionality': 'nationality',
        'father\'s_qualification': 'father_qualification',
        'mother\'s_qualification': 'mother_qualification' ,
       'mother\'s_occupation': 'mother_occupation', 
       'father\'s_occupation': 'father_occupation'
    })
    print(student.columns)
    # convert student grade to pass or fail
    
    os.chdir(owd)
    os.chdir("../../preparation_files")
    kee = ['marital_status', 'nationality', 'gender', 'admission_grade', 'age_at_enrollment', 'course', 'target'] 
    print(student.head())
    print(student['curricular_units_1st_sem_(evaluations)'].unique())
    print(len(student.columns))
    print(len(student))
    feats = [30, 25, 20, 15]
    records = [[4424, 3617, 2510, 1142], [4424, 3617, 2510, 1142], [4424, 3617, 2510, 1142], [4424, 3617, 2510, 1142]]

    for i in range(0, len(feats)):
        num_features_to_drop = 37 - feats[i]
        for record in records[i]:
            cath_copy = student.head(record)
            features_to_drop = [col for col in student.columns if col not in kee][:num_features_to_drop]
            cath_copy = cath_copy.drop(columns=features_to_drop)
            cath_copy.to_csv(f'datasets/dropout_{str(feats[i])}_{str(record)}.csv', index=False)
    
    # student.to_csv('datasets/dropout.csv', index=False)        


if __name__ == '__main__':
    # clean_adult()
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column widt
    clean_dropout()