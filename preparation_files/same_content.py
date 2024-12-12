import os
import pandas as pd
import numpy as np

def same_characteristics_v1(dataset_A, dataset_B, target_1, target_2):
    num_records_A = dataset_A.shape[0]
    num_attributes_A = dataset_A.shape[1]
    num_records_B = dataset_B.shape[0]
    num_attributes_B = dataset_B.shape[1]

    if num_records_A > num_records_B:
        dataset_A = dataset_A.sample(n=num_records_B, random_state=42)
    elif num_records_B > num_records_A:
        dataset_B = dataset_B.sample(n=num_records_A, random_state=42)

    # Categorize columns
    columns_A = categorize_columns(dataset_A, None)
    columns_B = categorize_columns(dataset_B, None)

    categorical_A = [col for col, typ in columns_A.items() if typ == 'Categorical' and col != target_1]
    continuous_A = [col for col, typ in columns_A.items() if typ == 'continuous']
    categorical_B = [col for col, typ in columns_B.items() if typ == 'Categorical' and col != target_2]
    continuous_B = [col for col, typ in columns_B.items() if typ == 'continuous']

    num_categorical_A = len(categorical_A)
    num_categorical_B = len(categorical_B)
    num_continuous_A = len(continuous_A)
    num_continuous_B = len(continuous_B)

    # Ensure the same number of categorical attributes
    if num_categorical_A > num_categorical_B:
        extra_categorical_A = num_categorical_A - num_categorical_B
        categorical_to_keep = categorical_A[:num_categorical_B]  # Keep first N categorical attributes
        additional_attributes_A = dataset_A[categorical_to_keep + continuous_A + [target_1]]
    elif num_categorical_B > num_categorical_A:
        extra_categorical_B = num_categorical_B - num_categorical_A
        categorical_to_keep = categorical_B[:num_categorical_A]  # Keep first N categorical attributes
        additional_attributes_B = dataset_B[categorical_to_keep + continuous_B + [target_2]]

    # Adjust number of continuous attributes if necessary
    if num_attributes_A > num_attributes_B:
        attributes_to_keep = [target_1]
        num_attributes_to_sample = num_attributes_B - 1  # Subtract target attribute count

        available_attributes_A = [col for col in dataset_A.columns if col != target_1 and col in categorical_to_keep + continuous_A]
        additional_attributes_A = dataset_A[available_attributes_A].sample(axis=1, n=num_attributes_to_sample, random_state=42)
        dataset_A = pd.concat([dataset_A[attributes_to_keep], additional_attributes_A], axis=1)
    elif num_attributes_B > num_attributes_A:
        attributes_to_keep = [target_2]
        num_attributes_to_sample = num_attributes_A - 1  # Subtract target attribute count

        available_attributes_B = [col for col in dataset_B.columns if col != target_2 and col in categorical_to_keep + continuous_B]
        additional_attributes_B = dataset_B[available_attributes_B].sample(axis=1, n=num_attributes_to_sample, random_state=42)
        dataset_B = pd.concat([dataset_B[attributes_to_keep], additional_attributes_B], axis=1)

    return dataset_A, dataset_B


def categorize_columns(df, continuous_to_categorical):
    results = {}
    total_rows = len(df)
    dynamic_threshold = round(np.log(total_rows) / np.log(np.log(total_rows)))
    if continuous_to_categorical is not None:
        for column in df.columns:
            unique_count = df[column].nunique()
            if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2 or (column in continuous_to_categorical):
                results[column] = 'Categorical'
            else:
                results[column] = 'continuous'
    else:
        for column in df.columns:
            unique_count = df[column].nunique()
            if df[column].dtype == 'object' or (unique_count < dynamic_threshold) or unique_count == 2:
                results[column] = 'Categorical'
            else:
                results[column] = 'continuous'
    return results

def find_max_unique_categorical(df, columns):
    categorical_columns = {k: v for k, v in columns.items() if v == 'Categorical'}
    unique_counts = {column: df[column].nunique() for column in categorical_columns}
    max_unique_column = max(unique_counts, key=unique_counts.get)
    max_unique_value = unique_counts[max_unique_column]
    return max_unique_column, max_unique_value

def adjust_unique_values(df_A, df_B, max_unique_value, the_letter):
    if the_letter == 'B':
        for column in df_A.columns:
            if df_A[column].nunique() > max_unique_value:
                # Find the most frequent values to keep
                top_values = df_A[column].value_counts().index[:max_unique_value]
                # print('NO NO')
                # print(top_values)
                # Randomly sample records to keep only those top values while minimizing record loss
                df_A = df_A[df_A[column].isin(top_values)]
    if the_letter == 'A':
        for column in df_B.columns:
            if df_B[column].nunique() > max_unique_value:
                # Find the most frequent values to keep
                top_values = df_B[column].value_counts().index[:max_unique_value]
                # print('YES YES')
                # print(top_values)
                # Randomly sample records to keep only those top values while minimizing record loss
                df_B = df_B[df_B[column].isin(top_values)]

    return df_A, df_B

def balance_records(df_A, df_B):
    num_records_A = len(df_A)
    num_records_B = len(df_B)

    if num_records_A > num_records_B:
        df_A = df_A.sample(n=num_records_B, random_state=42)
    elif num_records_B > num_records_A:
        df_B = df_B.sample(n=num_records_A, random_state=42)

    return df_A, df_B

def main(filename_1, filename_2, target_1, target_2, num_to_categ_1, num_to_categ_2):
    dataset_A = pd.read_csv('datasets/' + filename_1 + '.csv')
    dataset_B = pd.read_csv('datasets/' + filename_2 + '.csv')
    
    columns_A = categorize_columns(dataset_A, num_to_categ_1)
    columns_B = categorize_columns(dataset_B, num_to_categ_2)

    a, max_unique_value_A = find_max_unique_categorical(dataset_A, columns_A)
    b, max_unique_value_B = find_max_unique_categorical(dataset_B, columns_B)
    print("Before anything")
    print(f"max_unique_value_A is {max_unique_value_A}")
    print(b)
    print(f"max_unique_value_B is {max_unique_value_B}")
    print(f"len(dataset_A) is {len(dataset_A)}")
    print(f"len(dataset_B) is {len(dataset_B)}")
    print('\n')

    dataset_A, dataset_B = same_characteristics_v1(dataset_A, dataset_B, target_1, target_2)
    columns_A = categorize_columns(dataset_A, num_to_categ_1)
    columns_B = categorize_columns(dataset_B, num_to_categ_2)

    a, max_unique_value_A = find_max_unique_categorical(dataset_A, columns_A)
    b, max_unique_value_B = find_max_unique_categorical(dataset_B, columns_B)
    print("After same char v1")
    print(f"max_unique_value_A is {max_unique_value_A}")
    print(b)
    print(f"max_unique_value_B is {max_unique_value_B}")
    print(f"len(dataset_A) is {len(dataset_A)}")
    print(f"len(dataset_B) is {len(dataset_B)}")
    print('\n')
    common_max_unique_value= min(max_unique_value_A, max_unique_value_B)
    the_letter = 'A' if common_max_unique_value == max_unique_value_A else 'B'

    dataset_A, dataset_B = adjust_unique_values(dataset_A, dataset_B, common_max_unique_value, the_letter)
    
    a, max_unique_value_A = find_max_unique_categorical(dataset_A, columns_A)
    b, max_unique_value_B = find_max_unique_categorical(dataset_B, columns_B)
    print("After adjusting unique values")
    print(f"max_unique_value_A is {max_unique_value_A}")
    print(f"max_unique_value_B is {max_unique_value_B}")
    print(f"len(dataset_A) is {len(dataset_A)}")
    print(f"len(dataset_B) is {len(dataset_B)}")
    print('\n')

    dataset_A, dataset_B = same_characteristics_v1(dataset_A, dataset_B, target_1, target_2)
    # dataset_A, dataset_B = balance_records(dataset_A, dataset_B)
    # columns_A = categorize_columns(dataset_A, None)
    # columns_B = categorize_columns(dataset_B, None)
    # _, max_unique_value_A = find_max_unique_categorical(dataset_A, columns_A)
    # _, max_unique_value_B = find_max_unique_categorical(dataset_B, columns_B)
    # print("After balancing")
    # print(f"max_unique_value_A is {max_unique_value_A}")
    # print(f"max_unique_value_B is {max_unique_value_B}")
    # print(f"len(dataset_A) is {len(dataset_A)}")
    # print(f"len(dataset_B) is {len(dataset_B)}")
    # print('\n')

    the_baby_file_1 = filename_1 + '_(' + filename_2 + ')'
    the_baby_file_2 = filename_2 + '_(' + filename_1 + ')'
    # dataset_A.to_csv(f'datasets/{the_baby_file_1}.csv', index=False)
    # dataset_B.to_csv(f'datasets/{the_baby_file_2}.csv', index=False)

if __name__ == '__main__':
    main("Adult_v2", 'bank-full', 'income', 'subscription', None, ['day'])
