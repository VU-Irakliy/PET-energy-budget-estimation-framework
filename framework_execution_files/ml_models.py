import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, MaxAbsScaler, RobustScaler, PowerTransformer, QuantileTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, StackingRegressor
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from itertools import combinations
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.optimize import minimize
import sys
import io
import warnings
import lightgbm as lgb




def comp_func(actual_values):
    result = []
    for i in range(0, len(actual_values), 2):
        # Make sure there is a pair to compare
        if i + 1 < len(actual_values):
            first = actual_values[i]
            second = actual_values[i + 1]

            if first > second:
                result.append(0)
            elif first == second:
                result.append(2)
            else:
                result.append(1)
    return result


def regular_gbr(dataset, test_size, our_features, target, estimators, learning_rate, depth=3,  scalee = 0):

    split_index = int((1 - test_size) * len(dataset))
    X = dataset[list(our_features)]
    y = dataset[target]
    if scalee == 1:
            continuous_ones = [i for i in our_features if i != 'epsilon']

            X_scaled = X.copy()
            X_scaled[continuous_ones] = RobustScaler().fit_transform(X[continuous_ones])

            X_train = X_scaled.iloc[:split_index]
            X_test = X_scaled.iloc[split_index:]
            
    else:
        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]



    gb_model = GradientBoostingRegressor(n_estimators=estimators, learning_rate=learning_rate, max_depth=depth, random_state=42)
    gb_model.fit(X_train, y_train)

    y_pred = gb_model.predict(X_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    
    if len(y_pred) % 2 == 0:
        aa = []
        res_act = comp_func(y_test.reset_index(drop=True))
        res_pred = comp_func(y_pred)
        for i in range(len(res_act)):
            if res_act[i] == res_pred[i]:
                aa.append(True)
            else:
                aa.append(False)
        
        
        num = aa.count(True)
        length = len(aa)
        accuracy = (num / length) * 100
       
    else:
        print('Fix the test size for even number of values.')
        y_pred = 0
        y_test_2 = 0

    feature_importances = gb_model.feature_importances_

    importances = pd.Series(feature_importances, index=our_features)

  
    return gb_model, mse, r2,  accuracy



def light_gbr(our_data, our_features, target, perc, scalee, n_estimators=100, learning_rate=0.1, depth = -1, n_leaves = 31):
    warnings.simplefilter(action='ignore', category=UserWarning)
    test_size = perc
    split_index = int((1 - test_size) * len(our_data))
    X = our_data[list(our_features)]
    y = our_data[target]

    if scalee == 1:
        continuous_ones = [i for i in our_features if i != 'epsilon']
        X_scaled = X.copy()
        X_scaled[continuous_ones] = RobustScaler().fit_transform(X[continuous_ones])
        X_train = X_scaled.iloc[:split_index]
        X_test = X_scaled.iloc[split_index:]
    else:
        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = lgb.LGBMRegressor(n_estimators=n_estimators, learning_rate=learning_rate, random_state=42, verbose=-1)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)  # Ensure no negative predictions
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    if len(y_pred) % 2 == 0 and len(y_test) % 2 == 0:
        aa = []
        y_test_2 = y_test.reset_index(drop=True)
        y_pred_2 = pd.Series(y_pred).reset_index(drop=True)
        res_act = comp_func(y_test_2)
        res_pred = comp_func(y_pred_2)
        
        for i in range(len(res_act)):
            if res_act[i] == res_pred[i]:
                aa.append(True)
            else:
                aa.append(False)
        num = aa.count(True)
        length = len(aa)
        accuracy = (num / length) * 100
    else:
        aa = []
        accuracy = 0

    
    single_importances_series = pd.Series(model.feature_importances_ , index=our_features)
    importances_percentages = (single_importances_series / single_importances_series.sum())
    return model, mse, r2,  accuracy

def regular_reverse_gbr(our_data, our_features, target, perc, scalee, n_estimators=100, learning_rate=0.1, depth = 3):
    warnings.simplefilter(action='ignore', category=UserWarning)
    test_size = perc
    split_index = int(test_size * len(our_data))
    if split_index % 2 != 0:
        split_index += 1
    X = our_data[list(our_features)]
    y = our_data[target]

    if scalee == 1:
        continuous_ones = [i for i in our_features if i != 'epsilon']
        X_scaled = X.copy()
        X_scaled[continuous_ones] = RobustScaler().fit_transform(X[continuous_ones])
        X_train = X_scaled.iloc[split_index:]
        X_test = X_scaled.iloc[:split_index]
    else:
        X_train = X.iloc[split_index:]
        X_test = X.iloc[:split_index]

    y_train = y.iloc[split_index:]
    y_test = y.iloc[:split_index]

    model = GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=depth, random_state=42)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)  # Ensure no negative predictions
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    if len(y_pred) % 2 == 0 and len(y_test) % 2 == 0:
        aa = []
        y_test_2 = y_test.reset_index(drop=True)
        y_pred_2 = pd.Series(y_pred).reset_index(drop=True)
        res_act = comp_func(y_test_2)
        res_pred = comp_func(y_pred_2)
        
        for i in range(len(res_act)):
            if res_act[i] == res_pred[i]:
                aa.append(True)
            else:
                aa.append(False)
        num = aa.count(True)
        length = len(aa)
        accuracy = (num / length) * 100
    else:
        aa = []
        accuracy = 0

    
    single_importances_series = pd.Series(model.feature_importances_ , index=our_features)
    importances_percentages = (single_importances_series / single_importances_series.sum())
    return model, mse, r2,  accuracy
    

def light_reverse_gbr(our_data, our_features, target, perc, scalee, n_estimators=100, learning_rate=0.1, depth = -1, n_leaves = 31):
    warnings.simplefilter(action='ignore', category=UserWarning)
    test_size = perc
    split_index = int(test_size * len(our_data))
    if split_index % 2 != 0:
        split_index += 1
    X = our_data[list(our_features)]
    y = our_data[target]

    if scalee == 1:
        continuous_ones = [i for i in our_features if i != 'epsilon']
        X_scaled = X.copy()
        X_scaled[continuous_ones] = RobustScaler().fit_transform(X[continuous_ones])
        X_train = X_scaled.iloc[split_index:]
        X_test = X_scaled.iloc[:split_index]
    else:
        X_train = X.iloc[split_index:]
        X_test = X.iloc[:split_index]

    y_train = y.iloc[split_index:]
    y_test = y.iloc[:split_index]

    model = lgb.LGBMRegressor(n_estimators=n_estimators, learning_rate=learning_rate, random_state=42, verbose=-1)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)  # Ensure no negative predictions
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    if len(y_pred) % 2 == 0 and len(y_test) % 2 == 0:
        aa = []
        y_test_2 = y_test.reset_index(drop=True)
        y_pred_2 = pd.Series(y_pred).reset_index(drop=True)
        res_act = comp_func(y_test_2)
        res_pred = comp_func(y_pred_2)
        
        for i in range(len(res_act)):
            if res_act[i] == res_pred[i]:
                aa.append(True)
            else:
                aa.append(False)
        num = aa.count(True)
        length = len(aa)
        accuracy = (num / length) * 100
    else:
        aa = []
        accuracy = 0

    
    single_importances_series = pd.Series(model.feature_importances_ , index=our_features)
    importances_percentages = (single_importances_series / single_importances_series.sum())
    return model, mse, r2,  accuracy
    