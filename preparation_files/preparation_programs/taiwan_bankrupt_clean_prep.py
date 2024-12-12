
import pandas as pd
import os
import numpy as np


def clean_taiwan():
    owd = os.getcwd()
    os.chdir(owd)
    os.chdir("../../data/Taiwan_bankruptcy")
    #First, we handle regular taiwan.csv

    column_names = [
        'bankrupt', 'roa_c', 'roa_a', 'roa_b', 'op_gross_margin',
        'real_sales_gross_margin', 'op_profit_rate', 'pre_tax_net_int_rate', 'after_tax_net_int_rate', 'non_ind_income_expense_rev',
        'contingent_liabilities_equity', 'operating_income_capital', 'pre_tax_income_capital', 'working_capital_total_assets', 'quick_assets_total_assets',
        'current_assets_total_assets', 'cash_total_assets', 'quick_assets_current_liability', 'cash_current_liability', 'current_liability_assets',
        'operating_funds_liability', 'inventory_working_capital', 'inventory_current_liability', 'current_liabilities_liability', 'working_capital_equity',
        'current_liabilities_equity', 'lt_liability_current_assets', 'current_liability_current_assets', 'total_liability_exceeds_assets', 'equity_liability',
        'equity_total_assets', 'lt_liability_equity_fixed_assets', 'fixed_assets_assets', 'current_liability_liability', 'current_liability_equity',
        'equity_lt_liability', 'liability_equity', 'degree_financial_leverage', 'interest_coverage_ratio', 'operating_expenses_net_sales',
        'rnd_expenses_net_sales', 'effective_tax_rate', 'book_value_share_b', 'book_value_share_a', 'book_value_share_c',
        'cash_flow_share', 'sales_share', 'operating_income_share', 'sales_per_employee', 'operating_income_per_employee',
        'fixed_assets_per_employee', 'total_assets_gnp_price', 'return_on_total_assets_c', 'return_on_total_assets_a', 'return_on_total_assets_b',
        'gross_profit_net_sales', 'real_gross_profit_net_sales', 'operating_income_net_sales', 'pre_tax_income_net_sales', 'net_income_net_sales',
        'net_non_op_income_net_sales', 'net_income_exclude_disposal_gain_loss_net_sales', 'eps_net_income', 'pre_tax_income_share', 'ret_earnings_total_assets',
        'total_income_total_expenses', 'total_expenses_assets', 'net_income_total_assets', 'gross_profit_sales', 'net_income_equity',
        'net_income_negative_last_two_years', 'inventory_receivables_equity', 'total_asset_turnover', 'accounts_receivable_turnover', 'days_receivable_outstanding',
        'inventory_turnover', 'fixed_asset_turnover', 'equity_turnover', 'current_assets_sales', 'quick_assets_sales',
        'working_capital_sales', 'cash_sales', 'cash_flow_sales', 'no_credit_interval', 'cash_flow_operating_current_liabilities',
        'cash_flow_total_assets', 'cash_flow_liability', 'cfo_assets', 'cash_flow_equity', 'realized_gross_profit_growth_rate',
        'operating_income_growth', 'net_income_growth', 'continuing_operating_income_after_tax_growth', 'net_income_excluding_disposal_gain_loss_growth', 'total_asset_growth',
        'total_equity_growth', 'return_on_total_asset_growth'
    ]
    taiwan = pd.read_csv('data.csv', sep=',', names=column_names)
    taiwan = taiwan.drop(taiwan.index[0])
    taiwan = taiwan.drop( 'return_on_total_asset_growth', axis=1)
    # print(taiwan.head(10))
    # for column in taiwan.columns:
    #     unique_values = taiwan[column].dropna().unique()
    #     nan_count = taiwan[column].isna().sum()
    #     if nan_count > 0:
    #         print(f"Column {column}: Unique Values - {unique_values}, NaN Count - {nan_count}")
    # taiwan = taiwan.head(500)
    # for column in taiwan.columns:
    #     try:
    #         # Attempt to calculate the product of the column
    #         product = taiwan[column].prod()
    #         print(f"Column '{column}' calculated successfully with product: {product}")
    #     except Exception as e:
    #         # Catch and print the error with the column name
    #         print(f"Error in column '{column}': {str(e)}")
    
    print(len(taiwan.columns))
    print(len(taiwan))
    kee = ['current_assets_sales','working_capital_sales', 'quick_assets_sales', 'cash_sales', 'cash_flow_sales', 'cash_flow_operating_current_liabilities', 'bankrupt']
    os.chdir(owd)
    os.chdir("../../preparation_files")
    feats = [26, 16, 30]
    records = [[743, 1272, 1999, 2573, 3256, 4011], [1246, 2500, 3012, 4011], [793, 1592, 2386, 3257]]

    for i in range(0, len(feats)):
        num_features_to_drop = 96 - feats[i]
        for record in records[i]:
            cath_copy = taiwan.head(record)
            features_to_drop = [col for col in taiwan.columns if col not in kee][:num_features_to_drop]
            cath_copy = cath_copy.drop(columns=features_to_drop)
            cath_copy.to_csv(f'datasets/taiwan_{str(feats[i])}_{str(record)}.csv', index=False)
    
    exit()
    num_features_to_drop = 70
    features_to_drop = [col for col in taiwan.columns if col != 'bankrupt'][:num_features_to_drop]
    taiwan_2 = taiwan.drop(columns=features_to_drop)
 
   
    taiwan_2.to_csv('datasets/taiwan_bankrupt_2.csv', index=False)
    num_features_to_drop = 60
    features_to_drop = [col for col in taiwan.columns if col != 'bankrupt'][:num_features_to_drop]
    taiwan_2 = taiwan.drop(columns=features_to_drop)
 
   
    taiwan_2.to_csv('datasets/taiwan_bankrupt_3.csv', index=False)
    
    

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.max_rows', None)     # Display all rows
    pd.set_option('display.max_colwidth', None) # Display full column widt
    clean_taiwan()