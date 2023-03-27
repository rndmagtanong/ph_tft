import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             mean_absolute_error)
from sklearn.model_selection import GridSearchCV, train_test_split

pd.options.display.max_columns = 200
pd.options.display.max_rows = 200

def scoring(rf_grid, X_train, y_train, X_valid, y_valid):
    print(f'Train Accuracy - : {rf_grid.score(X_train, y_train):.3f}')
    print(f'Test Accuracy - : {rf_grid.score(X_valid, y_valid):.3f}')

    y_pred = rf_grid.best_estimator_.predict(X_valid)

    # mean absolute error

    mae = mean_absolute_error(y_valid, y_pred)

    # confusion matrix
    conf_mat = confusion_matrix(y_valid, y_pred)
    sns.heatmap(conf_mat, annot = True, fmt = 'g')
    plt.title('Confusion Matrix of Placement Predictor')
    plt.ylabel('Real Place')
    plt.xlabel('Predicted Place')
    plt.show()

    # accuracy score
    print("Accuracy of model:", accuracy_score(y_valid, y_pred))
    print("Mean Average Error: ", mae)

# read and concat data
X_chall = pd.read_csv('data/processed_challenger_match_data.csv')
X_gm = pd.read_csv('data/processed_gm_match_data.csv')
X_full = pd.concat([X_chall, X_gm], axis = 'index')

# remove duplicates
X_full = X_full.drop_duplicates().copy()

### Select subset of features

# filter columns
features = ['level', 'placement']

augs = re.compile("augments.")
trait_names = re.compile("traits_._name")
trait_nums = re.compile("traits_._num")
units_id = re.compile("units_._character")
units_rarity = re.compile("units_._rarity")
units_tier = re.compile("units_._tier")
itemnames = re.compile("units_._itemNames")
needed_columns = [augs, trait_names, trait_nums, units_id, units_rarity, units_tier, itemnames]

for filters in needed_columns:
    features += list(filter(filters.match, X_full.columns))

X = X_full[features]

# convert dtypes of discrete columns
for colname in list(X.select_dtypes("float64")):
    X[colname] = X[colname].astype(float).astype("Int64")

# create new feature for total item number
item_columns = [column for column in X.columns if 'item' in column]
X['total_items'] = X[item_columns].count(axis = 'columns').copy()
X = X.drop(item_columns, axis = 'columns')

# change NaNs of categoricals
X = X.fillna(0)

# one-hot encoding of categoricals
categoricals = [column for column in X.columns if ('augments' in column) or ('name' in column) or ('id' in column)]
X = pd.get_dummies(X, columns = categoricals)
X = X.replace(np.nan, 0)

# select target
y = X.placement
X = X.drop('placement', axis = 'columns')

# create classifications with 8 bins, 4 bins and 2 bins
X8 = X4 = X2 = X
y8 = y # 8 possible classifications
y4 = y.replace({1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4}) # 4 possible classifications
y2 = y.replace({1:1, 2:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2}) # 2 possible classifications

# create training and validation sets for y = 8 classes
X8_train, X8_valid, y8_train, y8_valid = train_test_split(X8, y8, test_size = 0.20, random_state = 0)
X4_train, X4_valid, y4_train, y4_valid = train_test_split(X4, y4, test_size = 0.20, random_state = 0)
X2_train, X2_valid, y2_train, y2_valid = train_test_split(X2, y2, test_size = 0.20, random_state = 0)

### build Random Forest Model with hyperparameters

# number of trees in random forest
n_estimators = [10, 100, 200]
# number of features to consider at every split
max_features = ['auto', 'sqrt']
# maximum number of levels in tree
max_depth = [None]
# minimum number of samples required to split a node
min_samples_split = [2,4]
# minimum number of samples required at each leaf node
min_samples_leaf = [1,2]
# method of selecting samples for training each tree
bootstrap = [True, False]

# create the random grid
param_grid = {
    'n_estimators' : n_estimators,
    'max_features' : max_features,
    'max_depth' : max_depth,
    'min_samples_split' : min_samples_split,
    'min_samples_leaf' : min_samples_leaf,
    'bootstrap' : bootstrap
}

# using RandomForestClassifier since placements are discrete values
forest_model = RandomForestClassifier()

# perform grid search for best parameters from param_grid above
rf_grid = GridSearchCV(estimator = forest_model, param_grid = param_grid, cv = 3, verbose = 2, n_jobs = 4)

# 8 classifications
rf_grid8 = rf_grid.fit(X8_train, y8_train)
rf_grid8.best_params_
scoring(rf_grid8, X8_train, y8_train, X8_valid, y8_valid) # Accuracy: 0.306

# 4 classifications
rf_grid4 = rf_grid.fit(X4_train, y4_train)
rf_grid4.best_params_
scoring(rf_grid4, X4_train, y4_train, X4_valid, y4_valid) # Accuracy: 0.550

# 2 classifications
rf_grid2 = rf_grid.fit(X2_train, y2_train)
rf_grid2.best_params_
scoring(rf_grid2, X2_train, y2_train, X2_valid, y2_valid) # Accuracy: 0.804