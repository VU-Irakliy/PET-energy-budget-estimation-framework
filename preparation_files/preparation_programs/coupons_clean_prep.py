
import pandas as pd
import os
import numpy as np


def clean_coupons():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Coupon Recommendation")
    #First, we handle regular coupons.csv
    coupons = pd.read_csv('in-vehicle-coupon-recommendation.csv', sep=',')
   
    # coupons = coupons.dropna()
    for column in coupons.columns:
        unique_values = coupons[column].dropna().unique()
        nan_count = coupons[column].isna().sum()
        if nan_count > 0:
            print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    coupons['car'] = coupons['car'].fillna('do not drive')
    coupons['Bar'] = coupons['Bar'].fillna('never')
    coupons['CoffeeHouse'] = coupons['CoffeeHouse'].fillna('never')
    coupons['CarryAway'] = coupons['CarryAway'].fillna('never')
    coupons['RestaurantLessThan20'] = coupons['RestaurantLessThan20'].fillna('never')
    coupons['Restaurant20To50'] = coupons['Restaurant20To50'].fillna('never')

    coupons = coupons.rename(columns={'Y': 'coupon_accepted', 'passanger': 'passenger'})
    print(coupons.head())
    print(coupons.info())
    coupons = coupons.head(2000)
    os.chdir(owd)
    os.chdir("../../preparation_files")

    coupons.to_csv('datasets/coupons.csv', index=False)
    
    

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column width
    clean_coupons()