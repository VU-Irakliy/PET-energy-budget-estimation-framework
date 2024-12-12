
import pandas as pd
import numpy as np

from scipy.stats import entropy, skew, kurtosis, moment

from numpy.linalg import svd


def compute_continuous_correlation(df, continuous_columns):
    """Computes mean and maximum continuous_correlation using the correlation matrix."""
    # Select only numeric columns to compute the correlation matrix
    numeric_df = df[continuous_columns]
    
    # Calculate the absolute correlation matrix
    correlation_matrix = numeric_df.corr().abs()

    # Since the diagonal values (correlation with self) are 1, we should exclude them
    np.fill_diagonal(correlation_matrix.values, 0)

    mean_continuous_correlation = correlation_matrix.mean().mean()
    max_continuous_correlation = correlation_matrix.max().max()
    
    return mean_continuous_correlation, max_continuous_correlation


def compute_data_complexity(df, categorical_columns):
    """Computes complexity metrics of the dataset."""
    
    if len(categorical_columns) > 0:
    # Shannon entropy for each categorical column
        entropy_metrics = {col: entropy(df[col].value_counts(normalize=True), base=2) 
                                        for col in categorical_columns}
        complexity_metrics = np.mean(list(entropy_metrics.values()))
    else:
        complexity_metrics = 0
    
    return complexity_metrics

def compute_distribution_metrics(df, continuous_columns):
    num_df = df[continuous_columns]
    """Computes distribution metrics for continuous attributes."""
    distribution_metrics = {
        'skewness': num_df.skew().mean(),
        'kurtosis': num_df.kurtosis().mean()
    }
    
    return distribution_metrics


def compute_dist_compl(original_dataset, categorical_columns, continuous_columns):
    complexity_metrics = compute_data_complexity(original_dataset, categorical_columns)
    if len(continuous_columns) > 0:
        distribution_metrics = compute_distribution_metrics(original_dataset, continuous_columns)


    
        std_dev = original_dataset[continuous_columns].std()
        variance = original_dataset[continuous_columns].var()

        mean_std_dev = std_dev.mean()
        mean_variance = variance.mean()

        max_std_dev = std_dev.max()
        max_variance = variance.max()
    else:
        distribution_metrics = {
            'skewness': 0,
            'kurtosis': 0
        }
        std_dev = 0
        variance = 0

        mean_std_dev = 0
        mean_variance = 0

        max_std_dev = 0
        max_variance = 0


    mean_continuous_correlation, max_continuous_correlation = compute_continuous_correlation(original_dataset, continuous_columns)

    return complexity_metrics, distribution_metrics, mean_std_dev,  mean_variance, max_std_dev, max_variance, mean_continuous_correlation, max_continuous_correlation

def convert_to_categorical(df, misclassified_attributes, target):
    """
    Convert columns in misclassified_attributes list to categorical type.
    """
    if misclassified_attributes == None:
        aaaa = [target]
    else:
        aaaa  = misclassified_attributes + [target]
    for col in aaaa:
        if col in df.columns:
            df[col] = df[col].astype('category')  # Convert to categorical data type
    return df




def class_imbalance_ratio(y):
    class_counts = y.value_counts()
    majority_class = class_counts.max()
    minority_class = class_counts.min()
    imbalance_ratio = majority_class / minority_class
    return imbalance_ratio

def percentage_of_outliers(df):
    outliers = 0
    total_values = np.product(df.shape)
    continuous_df = df.select_dtypes(include=[np.number]) #since categorical numerical columns have been converted to categorical, those will be excluded
    if continuous_df.empty:
        return 0
    
    for col in continuous_df: 
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers += df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
    
    outlier_percentage = (outliers / total_values) * 100
    return outlier_percentage

def average_cat_uniquness_ratio_ratio(df):
    cat_uniquness_ratio_ratios = []
    
    categorical_df = df.select_dtypes(include=['object', 'category'])
    if categorical_df.empty:
        return 0
    
    for col in  categorical_df :  
        num_unique_values = df[col].nunique()
        num_total_values = len(df[col])
        cat_uniquness_ratio_ratio = num_unique_values / num_total_values
        cat_uniquness_ratio_ratios.append(cat_uniquness_ratio_ratio)
    
    avg_cat_uniqueness_ratio_ratio = np.mean(cat_uniquness_ratio_ratios)
    return avg_cat_uniqueness_ratio_ratio






def print_constant_columns(df, threshold=1e-8):
    """
    Print the columns in the DataFrame that are constant or nearly constant, ignoring categorical columns.
    
    Parameters:
    - df: DataFrame to check for constant columns.
    - threshold: Variance threshold below which a column is considered constant.
    """
    # Select only continuous columns for this operation
    continuous_df = df.select_dtypes(include=[np.number]) #since categorical numerical columns have been converted to categorical, those will be excluded
    
    # Find constant columns
    constant_columns = continuous_df.columns[(continuous_df.max() - continuous_df.min()).abs() <= threshold]
    
    if len(constant_columns) > 0:
        print("Constant or nearly constant columns:")
        for col in constant_columns:
            print(f"- {col}")
    else:
        print("No constant or nearly constant columns found.")


def drop_constant_continuous_columns(df, threshold=1e-8):
    # Select continuous columns
    continuous_columns = df.select_dtypes(include=[np.number]).columns #since categorical numerical columns have been converted to categorical, those will be excluded
    
    # Create a boolean mask for continuous columns that are non-constant
    non_constant_mask = (df[continuous_columns].max() - df[continuous_columns].min()).abs() > threshold
    
    # Filter the continuous columns that are non-constant
    non_constant_continuous_columns = continuous_columns[non_constant_mask]
    
    # Return the original DataFrame with non-constant continuous columns
    # and all non-continuous columns (i.e., categorical, etc.)
    return df[list(non_constant_continuous_columns) + df.select_dtypes(exclude=[np.number]).columns.tolist()]


def achieve_more_data(files, categorical, targets):
    records =[

    ]
    for i in range(len(files)):
        df = pd.read_csv(f'datasets/{files[i]}.csv')
        df = convert_to_categorical(df, categorical[i], targets[i])
        # print_constant_columns(df)
        
        df = drop_constant_continuous_columns(df)

        imbalance_ratio = class_imbalance_ratio(df[targets[i]])
        outlier_percentage = percentage_of_outliers(df)
        avg_cat_uniqueness_ratio = average_cat_uniquness_ratio_ratio(df)
        for j in range(2):
            records.append(
                {'dataset_name': files[i], 
                 'imbalance_ratio': imbalance_ratio, 
                 'outlier_percentage': outlier_percentage,
                'avg_cat_uniqueness_ratio': avg_cat_uniqueness_ratio,
            })
    
    all_records = pd.DataFrame(records)
    all_records.to_csv('additional_dataset_properties.csv', index=False)
    print("The additional properties of the datasets have been saved to 'additional_dataset_properties.csv'.")






