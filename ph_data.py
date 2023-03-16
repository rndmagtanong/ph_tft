import pandas as pd
import requests
from flatten_json import flatten

def get_challengers(api_key: 'string') -> 'json':
    ph_challengers_url =  'https://ph2.api.riotgames.com/tft/league/v1/challenger'
    ph_challengers_url = ph_challengers_url + '?api_key=' + api_key

    ph_challengers_resp = requests.get(ph_challengers_url)
    challengers_info = ph_challengers_resp.json()
    return challengers_info

def get_gms(api_key):
    ph_gm_url = 'https://ph2.api.riotgames.com/tft/league/v1/grandmaster'
    ph_gm_url = ph_gm_url + '?api_key=' + api_key

    ph_gm_resp = requests.get(ph_gm_url)
    gm_info = ph_gm_resp.json()
    return gm_info

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
        puuid_resp = requests.get(puuid_url)
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
        match_resp = requests.get(match_url)
        match_ids += match_resp.json()

    return match_ids

def get_match_data(match_ids):
    holder = pd.DataFrame()
    for match in match_ids:
        match_url = 'https://sea.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + api_key
        match_resp = requests.get(match_url).json()

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

        # player1 = player1.merge(player2, how = 'outer', left_index = True)
        # player1 = player1.merge(player3, how = 'outer', left_index = True)
        # player1 = player1.merge(player4, how = 'outer', left_index = True)
        # player1 = player1.merge(player5, how = 'outer', left_index = True)
        # player1 = player1.merge(player6, how = 'outer', left_index = True)
        # player1 = player1.merge(player7, how = 'outer', left_index = True)
        # player1 = player1.merge(player8, how = 'outer', left_index = True)

        holder = pd.concat([holder, player1], ignore_index = True)
        holder = pd.concat([holder, player2], ignore_index = True)
        holder = pd.concat([holder, player3], ignore_index = True)
        holder = pd.concat([holder, player4], ignore_index = True)
        holder = pd.concat([holder, player5], ignore_index = True)
        holder = pd.concat([holder, player6], ignore_index = True)
        holder = pd.concat([holder, player7], ignore_index = True)
        holder = pd.concat([holder, player8], ignore_index = True)

    return holder

def simple_pipeline(match_data, filename):
    # drop columns from double up
    match_data = match_data[match_data.partner_group_id.isnull()]

    # drop all empty rows and columns
    match_data.dropna(how = 'all').dropna(axis = 'columns', how = 'all')

    # write csv for data analysis
    match_data.to_csv('unprocessed_' + filename, index = True)

    # remove features that don't help with training the data
    non_training_features = ['companion_content_ID', 'companion_item_ID',
                             'companion_skin_ID', 'companion_species',
                             'gold_left', 'players_eliminated']
    for feature in non_training_features:
        try:
            match_data.drop(feature, axis = 'columns', inplace = True)
        except:
            continue

    # write csv for placement estimator
    match_data.to_csv('processed_' + filename, index = True)

if __name__ == "__main__":

    print('Enter API key:')
    api_key = input()

    challengers = get_challengers(api_key)
    chall_names = get_names(challengers)
    chall_puuids = get_puuid(chall_names)
    chall_matches = get_match_ids(chall_puuids)
    # remove duplicate matches
    chall_matches = list(dict.fromkeys(chall_matches))
    chall_match_data = get_match_data(chall_matches)
    chall_match_data.to_csv('chall_match_data.csv', index = True)

    gms = get_gms(api_key)
    gm_names = get_names(gms)
    gm_puuids = get_puuid(gm_names)
    gm_matches = get_match_ids(gm_puuids)
    gm_matches = list(dict.fromkeys(gm_matches))
    gm_match_data = get_match_data(gm_matches)
    gm_match_data.to_csv('gm_match_data.csv', index = True)




