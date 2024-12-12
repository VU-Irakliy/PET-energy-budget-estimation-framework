
import pandas as pd
import os
import numpy as np





"""
10-11          0-9
(sufficient)   (fail)
D                 F
(from the paper Cortez, P. and A. M. Gonçalves Silva. “Using data mining to predict secondary school student performance.” (2008).)

Therefore, minimum passing grade is 10!

"""

def clean_student():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Student")
    student = pd.read_csv('student-por.csv', sep=';')
    

    # convert student grade to pass or fail
    student.loc[student['G3'] < 10, 'G3'] = 0
    student.loc[student['G3'] > 9, 'G3'] = 1
    student['G3'] = student['G3'].astype(int)

    os.chdir(owd)
    os.chdir("../preparation_files")

    print(student.head())

    student.to_csv('datasets/student-por.csv', index=False)        


if __name__ == '__main__':
    # clean_adult()
    clean_student()