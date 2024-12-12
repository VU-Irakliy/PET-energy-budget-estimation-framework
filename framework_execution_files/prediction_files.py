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

from framework_execution_files.retrieve_data import *
from framework_execution_files.ml_models import *



def get_energy_synthesis_pred(records, dataset_data, epsilon ):


    features = ['epsilon', 'num_attributes', 'num_records', 'max_categorical_unique', 'mean_std_dev']


    model, accuracy_mse, accuracy_r2, accuracy_comp = regular_gbr(records, 0.19, features, 'energy', 100, 0.1)
    input_data = {feature: dataset_data[feature] for feature in features}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    prediction = np.clip(prediction, a_min=0, a_max=None)

    return prediction[0], accuracy_r2



def get_singling_out_risk_pred(records, dataset_data, epsilon):

    features = ['epsilon', 'skewness', 'mean_continuous_correlation', 'outlier_percentage', 'max_continuous_correlation', 
                   'kurtosis', 'size_mb', 'avg_cat_uniqueness_ratio', 'entropy', 'max_std_dev', 'num_records', 'imbalance_ratio', 
                   'num_attributes', 'mean_categorical_unique']
    model, accuracy_mse, accuracy_r2, accuracy_comp = light_gbr(records, features, 'singling_out_risk', 0.19, 0, n_estimators=100, learning_rate=0.1, depth = -1)
    input_data = {feature: dataset_data[feature] for feature in features}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    prediction = np.clip(prediction, a_min=0, a_max=None)

    return prediction[0], accuracy_r2





def get_logres_accuracy_prediction(records, dataset_data, epsilon ):
    
    features = ['epsilon', 'imbalance_ratio', 'skewness', 'mean_continuous_correlation', 'size_mb',
                    'kurtosis', 'max_continuous_correlation', 'avg_cat_uniqueness_ratio', 'max_categorical_unique']
    model, accuracy_mse, accuracy_r2, accuracy_comp = regular_reverse_gbr(records,features,  'accuracy_logres', 0.19, 0,    100, 0.1, 3)
    
    input_data = {feature: dataset_data[feature] for feature in features}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    prediction = np.clip(prediction, a_min=0, a_max=None)

    return prediction[0], accuracy_r2
    ...




def get_knn_accuracy_prediction(records, dataset_data, epsilon ):
   
    features = ['epsilon', 'size_mb', 'outlier_percentage', 'num_records', 
                   'num_continuous_attributes', 'skewness', 'mean_continuous_correlation', 'imbalance_ratio', 'kurtosis']
    model, accuracy_mse, accuracy_r2, accuracy_comp = light_reverse_gbr(records, features, 'accuracy_knn', 0.19, 0, n_estimators=100, learning_rate=0.1, depth = -1)
    input_data = {feature: dataset_data[feature] for feature in features}
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    prediction = np.clip(prediction, a_min=0, a_max=None)

    return prediction[0], accuracy_r2
    ...