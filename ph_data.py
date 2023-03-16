import pandas as pd
import numpy as np
import requests
from flatten_json import flatten

def get_challengers(api_key: 'string') -> 'json':
    ph_challengers_url =  'https://ph2.api.riotgames.com/tft/league/v1/challenger'
    ph_challengers_url = ph_challengers_url + '?api_key=' + api_key

    try:
        ph_challengers_resp = requests.get(ph_challengers_url, timeout = 127)
        challengers_info = ph_challengers_resp.json()
        return challengers_info
    except:
        print('Request has timed out.')

def get_gms(api_key):
    ph_gm_url = 'https://ph2.api.riotgames.com/tft/league/v1/grandmaster'
    ph_gm_url = ph_gm_url + '?api_key=' + api_key

    try:
        ph_gm_resp = requests.get(ph_gm_url, timeout = 127)
        gm_info = ph_gm_resp.json()
        return gm_info
    except:
        print('Request has timed out.')

def get_names(players):
    player_names = []
    players = players.get('entries')
    for i in range(len(players)):
        if (players[i])['wins'] != 0:
            player_names += [(players[i]).get('summonerName')]

    return player_names

def get_puuid(names):
    puuids = []
    for name in names:
        puuid_url = 'https://ph2.api.riotgames.com/tft/summoner/v1/summoners/by-name/'
        puuid_url = puuid_url + name + '?api_key=' + api_key
        puuid_resp = requests.get(puuid_url, timeout = 127)
        puuids += [dict(puuid_resp.json())]

    final_puuids = []
    for i in range(len(puuids)):
        final_puuids += [puuids[i].get('puuid')]

    return final_puuids

def get_match_ids(puuids):
    match_ids = []
    for puuid in puuids:
        match_url = 'https://sea.api.riotgames.com/tft/match/v1/matches/by-puuid/'
        match_url += puuid + '/ids?start=0&count=50&api_key=' + api_key
        match_resp = requests.get(match_url, timeout = 127)
        match_ids += match_resp.json()

    return match_ids

def get_match_data(match_ids):

    match_data = pd.DataFrame()

    for match in match_ids:
        match_url = 'https://sea.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + api_key
        match_resp = requests.get(match_url, timeout = 127).json()

        flat_match_resp = flatten(match_resp)
        keyList = list(flat_match_resp.keys())

        keyList1 = [key for key in keyList if key.startswith('info_participants_0')]
        keyList2 = [key for key in keyList if key.startswith('info_participants_1')]
        keyList3 = [key for key in keyList if key.startswith('info_participants_2')]
        keyList4 = [key for key in keyList if key.startswith('info_participants_3')]
        keyList5 = [key for key in keyList if key.startswith('info_participants_4')]
        keyList6 = [key for key in keyList if key.startswith('info_participants_5')]
        keyList7 = [key for key in keyList if key.startswith('info_participants_6')]
        keyList8 = [key for key in keyList if key.startswith('info_participants_7')]

        player1info = {k:v for k, v in flat_match_resp.items() if k in keyList1}
        player2info = {k:v for k, v in flat_match_resp.items() if k in keyList2}
        player3info = {k:v for k, v in flat_match_resp.items() if k in keyList3}
        player4info = {k:v for k, v in flat_match_resp.items() if k in keyList4}
        player5info = {k:v for k, v in flat_match_resp.items() if k in keyList5}
        player6info = {k:v for k, v in flat_match_resp.items() if k in keyList6}
        player7info = {k:v for k, v in flat_match_resp.items() if k in keyList7}
        player8info = {k:v for k, v in flat_match_resp.items() if k in keyList8}

        player1 = pd.DataFrame([player1info])
        player2 = pd.DataFrame([player2info])
        player3 = pd.DataFrame([player3info])
        player4 = pd.DataFrame([player4info])
        player5 = pd.DataFrame([player5info])
        player6 = pd.DataFrame([player6info])
        player7 = pd.DataFrame([player7info])
        player8 = pd.DataFrame([player8info])

        player1.columns = player1.columns.str.replace('info_participants_0_', '')
        player2.columns = player2.columns.str.replace('info_participants_1_', '')
        player3.columns = player3.columns.str.replace('info_participants_2_', '')
        player4.columns = player4.columns.str.replace('info_participants_3_', '')
        player5.columns = player5.columns.str.replace('info_participants_4_', '')
        player6.columns = player6.columns.str.replace('info_participants_5_', '')
        player7.columns = player7.columns.str.replace('info_participants_6_', '')
        player8.columns = player8.columns.str.replace('info_participants_7_', '')

        player1 = player1.convert_dtypes()
        player2 = player2.convert_dtypes()
        player3 = player3.convert_dtypes()
        player4 = player4.convert_dtypes()
        player5 = player5.convert_dtypes()
        player6 = player6.convert_dtypes()
        player7 = player7.convert_dtypes()
        player8 = player8.convert_dtypes()

        player1 = player1.select_dtypes(exclude=['object'])
        player2 = player2.select_dtypes(exclude=['object'])
        player3 = player3.select_dtypes(exclude=['object'])
        player4 = player4.select_dtypes(exclude=['object'])
        player5 = player5.select_dtypes(exclude=['object'])
        player6 = player6.select_dtypes(exclude=['object'])
        player7 = player7.select_dtypes(exclude=['object'])
        player8 = player8.select_dtypes(exclude=['object'])

        match_data = pd.concat([match_data, player1], ignore_index = True)
        match_data = pd.concat([match_data, player2], ignore_index = True)
        match_data = pd.concat([match_data, player3], ignore_index = True)
        match_data = pd.concat([match_data, player4], ignore_index = True)
        match_data = pd.concat([match_data, player5], ignore_index = True)
        match_data = pd.concat([match_data, player6], ignore_index = True)
        match_data = pd.concat([match_data, player7], ignore_index = True)
        match_data = pd.concat([match_data, player8], ignore_index = True)

    return match_data

### data pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class DoubleUpDropper(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        return X[X['partner_group_id'].isnull()]
    
class NaNDropper(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        return X.dropna(how = 'all').dropna(axis = 'columns', how = 'all')
    
class CorruptedDropper(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        corrupted_features = ['units_5_items_0', 'units_5_items_1',	
                            'units_5_items_2', 'units_6_items_0',
                            'units_6_items_1', 'units_6_items_2',
                            'units_7_items_0', 'units_7_items_1',	
                            'units_7_items_2', 'units_3_items_0',
                            'units_3_items_1', 'units_0_items_0',
                            'units_1_items_0', 'units_1_items_1',	
                            'units_2_items_0', 'units_2_items_1',	
                            'units_2_items_2', 'units_1_items_2',
                            'units_4_items_0', 'units_4_items_1',	
                            'units_4_items_2', 'units_0_items_1',	
                            'units_3_items_2', 'units_0_items_2',	
                            'units_8_items_0', 'units_8_items_1',	
                            'units_8_items_2']
        for feature in corrupted_features:
            try:
                X = X.drop(feature, axis = 'columns')
            except:
                continue

            return X
        
class ResetIndex(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        return X.reset_index(drop = True)

class DescribeMissing(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        # get number of missing data points per column
        missing_values_count = X.isnull().sum()

        # how many missing values do we have?
        total_cells = np.product(X.shape)
        total_missing = missing_values_count.sum()

        # percent of missing data
        percent_missing = (total_missing / total_cells) * 100
        print('Percent Missing of Data: ' + str(percent_missing))

        return X
    
from sklearn.pipeline import Pipeline

pipe_analysis = Pipeline([
       ("double_up_dropper", DoubleUpDropper()),
       ("nandrop", NaNDropper()),
       ("corruptdropper", CorruptedDropper()),
       ("resetindex", ResetIndex()),
       ("nanpercent", DescribeMissing())
])

class TrainDropper(BaseEstimator, TransformerMixin):

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        # remove features that don't help with training the data
        non_training_features = ['companion_content_ID', 'companion_item_ID',
                                'companion_skin_ID', 'companion_species',
                                'gold_left', 'players_eliminated']
        
        for feature in non_training_features:
            try:
                X = X.drop(feature, axis = 'columns')
            except:
                continue
        
        return X
    
class OutlierRemover(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        # remove outliers (10% threshold to not remove level 8 data)
        threshold = int(len(X) * 0.1)
        X = X.dropna(axis = 1, thresh = threshold)
        
        return X

class GetAugmentDummies(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        augments = ['augments_0', 'augments_1', 'augments_2']
        X = pd.get_dummies(X, columns = augments)

        return X

pipe_ml = Pipeline([
        ("name_dropper", TrainDropper()),
        ("outlier_dropper", OutlierRemover()),
        ("augmentdummies", GetAugmentDummies())
])

def use_data_pipeline(match_data, filename):

    # use pipeline for data analysis
    pipe_analysis = Pipeline([
       ("double_up_dropper", DoubleUpDropper()),
       ("nandrop", NaNDropper()),
       ("corruptdropper", CorruptedDropper()),
       ("resetindex", ResetIndex()),
       ("nanpercent", DescribeMissing())
    ])

    match_data = pipe_analysis.fit_transform(match_data)

    # write csv for data analysis
    match_data.to_csv('unprocessed_' + filename + '.csv', index = False)

    pipe_ml = Pipeline([
            ("name_dropper", TrainDropper()),
            ("outlier_dropper", OutlierRemover()),
            ("augmentdummies", GetAugmentDummies())
    ])

    match_data = pipe_ml.fit_transform(match_data)

    # write csv for placement estimator
    match_data.to_csv('processed_' + filename + '.csv', index = False)

    return match_data

if __name__ == "__main__":

    print('Enter API key:')
    api_key = ''

    while api_key == '':
        api_key = str(input())

    try:
        challengers = get_challengers(api_key)
        chall_names = get_names(challengers)
        chall_puuids = get_puuid(chall_names)
        chall_matches = get_match_ids(chall_puuids)
        # remove duplicate matches
        chall_matches = list(dict.fromkeys(chall_matches))
        chall_match_data = get_match_data(chall_matches)

        processed_chall_match_data = use_data_pipeline(chall_match_data, 'challenger_match_data')

        gms = get_gms(api_key)
        gm_names = get_names(gms)
        gm_puuids = get_puuid(gm_names)
        gm_matches = get_match_ids(gm_puuids)
        gm_matches = list(dict.fromkeys(gm_matches))
        gm_match_data = get_match_data(gm_matches)

        processed_gm_match_data = use_data_pipeline(gm_match_data, 'gm_match_data')
        
    except:
        print('Error occurred during ETL process.')




