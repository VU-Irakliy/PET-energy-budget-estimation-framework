import numpy as np


def categorize_columns(df, continuous_to_categorical):
        results = {}
        total_rows = len(df)
        dynamic_threshold = round(np.log(total_rows) / np.log(np.log(total_rows)) )
        if continuous_to_categorical != None:
            for column in df.columns:
                unique_count = df[column].nunique()
                if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2  or (column in continuous_to_categorical):
                    results[column] = 'Categorical'
                else:
                    # print(column)
                    # print(df[column].dtype)
                    results[column] = 'continuous'
        else:
            for column in df.columns:
                unique_count = df[column].nunique()
                if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2:
                    results[column] = 'Categorical'
                else:
                    # print(column)
                    # print(df[column].dtype)
                    results[column] = 'continuous'

        
        return results



    

def find_max_unique_categorical(df, columns):

    categorical_columns = {k: v for k, v in columns.items() if v == 'Categorical'}

    unique_counts = {column: df[column].nunique() for column in categorical_columns}

    max_unique_column = max(unique_counts, key=unique_counts.get)
    max_unique_value = unique_counts[max_unique_column]

    return max_unique_value


   