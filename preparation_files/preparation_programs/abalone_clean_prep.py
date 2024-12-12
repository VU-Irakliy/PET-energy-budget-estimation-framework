import os
import pandas as pd

def clean_prep_abalone():
    def age_category(rings):
        if rings <= 8:
            return 'Young' # 0 - Young
        elif rings <= 15:
            return 'Adult' # 1 - Adult
        else:
            return 'Old' # 2 - Old
    

    
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../data/Abalone")

    columns = ['sex', 'length', 'diameter', 'height','whole_weight', 'shucked_weight', 'viscera_weight', 'shell_weight', 'rings']

    abalone_data = pd.read_csv("abalone.data", sep=",",names=columns,na_values=["?"], engine='python')
    print(abalone_data.head())
    abalone_data = abalone_data.dropna()

    abalone_data['age_category'] = abalone_data['rings'].apply(age_category)
    print(abalone_data['rings'].max())

    abalone_data.drop('rings', axis=1, inplace=True)
    print(abalone_data.head())
    os.chdir(owd)
    os.chdir("../preparation_files")

    abalone_data.to_csv('datasets/abalone.csv', index=False)





if __name__ == '__main__':
    clean_prep_abalone()