import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
pd.options.display.max_columns = 200
pd.options.display.max_rows = 200

# read and concat data
X_chall = pd.read_csv('processed_challenger_match_data.csv')
X_gm = pd.read_csv('processed_gm_match_data.csv')
X_full = pd.concat([X_chall, X_gm], axis = 'index')

# remove duplicates
X_full = X_full.drop_duplicates().copy()

# Select subset of predictors
cols_to_use = \
['augments_0',
 'augments_1',
 'augments_2',
#  'last_round',
 'level',
 'placement', # <--- this is the target
#  'puuid',
#  'time_eliminated',
#  'total_damage_to_players',
 'traits_0_name',
 'traits_0_num_units',
#  'traits_0_style',
#  'traits_0_tier_current',
#  'traits_0_tier_total',
 'traits_1_name',
 'traits_1_num_units',
#  'traits_1_style',
#  'traits_1_tier_current',
#  'traits_1_tier_total',
 'traits_2_name',
 'traits_2_num_units',
#  'traits_2_style',
#  'traits_2_tier_current',
#  'traits_2_tier_total',
 'traits_3_name',
 'traits_3_num_units',
#  'traits_3_style',
#  'traits_3_tier_current',
#  'traits_3_tier_total',
 'traits_4_name',
 'traits_4_num_units',
#  'traits_4_style',
#  'traits_4_tier_current',
#  'traits_4_tier_total',
 'traits_5_name',
 'traits_5_num_units',
#  'traits_5_style',
#  'traits_5_tier_current',
#  'traits_5_tier_total',
 'traits_6_name',
 'traits_6_num_units',
#  'traits_6_style',
#  'traits_6_tier_current',
#  'traits_6_tier_total',
 'traits_7_name',
 'traits_7_num_units',
#  'traits_7_style',
#  'traits_7_tier_current',
#  'traits_7_tier_total',
 'traits_8_name',
 'traits_8_num_units',
#  'traits_8_style',
#  'traits_8_tier_current',
#  'traits_8_tier_total',
 'traits_9_name',
 'traits_9_num_units',
#  'traits_9_style',
#  'traits_9_tier_current',
#  'traits_9_tier_total',
 'traits_10_name',
 'traits_10_num_units',
#  'traits_10_style',
#  'traits_10_tier_current',
#  'traits_10_tier_total',
 'units_0_character_id',
#  'units_0_name',
 'units_0_rarity',
 'units_0_tier',
 'units_1_character_id',
 'units_1_itemNames_0',
#  'units_1_name',
 'units_1_rarity',
 'units_1_tier',
 'units_2_character_id',
#  'units_2_name',
 'units_2_rarity',
 'units_2_tier',
 'units_3_character_id',
#  'units_3_name',
 'units_3_rarity',
 'units_3_tier',
 'units_4_character_id',
 'units_4_itemNames_0',
 'units_4_itemNames_1',
#  'units_4_name',
 'units_4_rarity',
 'units_4_tier',
 'units_5_character_id',
 'units_5_itemNames_0',
 'units_5_itemNames_1',
#  'units_5_name',
 'units_5_rarity',
 'units_5_tier',
 'units_6_character_id',
 'units_6_itemNames_0',
 'units_6_itemNames_1',
#  'units_6_name',
 'units_6_rarity',
 'units_6_tier',
 'units_7_character_id',
 'units_7_itemNames_0',
 'units_7_itemNames_1',
 'units_7_itemNames_2',
#  'units_7_name',
 'units_7_rarity',
 'units_7_tier',
 'units_8_character_id',
#  'units_8_name',
 'units_8_rarity',
 'units_8_tier',
#  'traits_11_name',
 'traits_11_num_units',
#  'traits_11_style',
#  'traits_11_tier_current',
#  'traits_11_tier_total',
 'traits_12_name',
 'traits_12_num_units',
#  'traits_12_style',
#  'traits_12_tier_current',
#  'traits_12_tier_total',
 'units_2_itemNames_0',
 'units_2_itemNames_1',
 'units_2_itemNames_2',
 'units_5_itemNames_2',
 'units_0_itemNames_0',
 'units_3_itemNames_0',
 'units_3_itemNames_1',
 'units_3_itemNames_2',
 'units_4_itemNames_2',
 'units_6_itemNames_2',
 'units_0_itemNames_1',
 'units_0_itemNames_2',
 'units_1_itemNames_1',
 'units_1_itemNames_2',
 'units_8_itemNames_0',
 'traits_13_name',
 'traits_13_num_units',
#  'traits_13_style',
#  'traits_13_tier_current',
#  'traits_13_tier_total',
 'units_8_itemNames_1']

X = X_full[cols_to_use]

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

###

# Create training and validation sets
from sklearn.model_selection import train_test_split

X_train, X_valid, y_train, y_valid = train_test_split(X, y)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error

forest_model = RandomForestClassifier(random_state = 1)
forest_model.fit(X_train, y_train)
place_preds = forest_model.predict(X_valid)
print(mean_absolute_error(y_valid, place_preds))

# Cross validation attempt

from sklearn.pipeline import Pipeline

my_pipeline = Pipeline(steps=[
    ('model', RandomForestClassifier(n_estimators = 50, random_state = 0))
])

from sklearn.model_selection import cross_val_score
# Multiply by -1 since sklearn calculates *negative* MAE
scores = -1 * cross_val_score(my_pipeline, X, y,
                              cv = 5,
                              scoring='neg_mean_absolute_error')

print("MAE scores:\n", scores)

print("Average MAE score (across experiments):")
print(scores.mean())

# confusion matrix
from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_valid, place_preds)
sns.heatmap(conf_mat, annot = True, fmt = 'g')
plt.title('Confusion Matrix of Placement Predictor')
plt.ylabel('Real Place')
plt.xlabel('Predicted Place')
plt.show()