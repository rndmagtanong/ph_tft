import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
plt.style.use('ggplot')
pd.options.display.max_columns = 200
pd.options.display.max_rows = 200

ph_tft_challenger_data = pd.read_csv('unprocessed_challenger_match_data.csv')
ph_tft_gm_data = pd.read_csv('unprocessed_gm_match_data.csv')

# merge dataframes
merged_data = pd.concat([ph_tft_challenger_data, ph_tft_gm_data], ignore_index = True)

# drop duplicate matches
merged_data = merged_data.drop_duplicates()

# look at dtypes
print(merged_data.dtypes)

# describe the data
merged_data.describe()

### Exploratory Data Analysis

# remove columns we don't need
columns = list(merged_data.columns)

# for illustration only, here are the features that will remain
wanted_columns = [
                'augments_0',
                'augments_1',
                'augments_2',
    #            'companion_content_ID',
    #            'companion_item_ID',
    #            'companion_skin_ID',
                'companion_species',
                'gold_left',
    #            'last_round',
                'level',
                'placement',
    #            'players_eliminated',
                'puuid',
    #            'time_eliminated',
    #            'total_damage_to_players',
                'traits_0_name',
                'traits_0_num_units',
    #            'traits_0_style',
    #            'traits_0_tier_current',
    #            'traits_0_tier_total',
                'traits_1_name',
                'traits_1_num_units',
    #           'traits_1_style',
    #            'traits_1_tier_current',
    #            'traits_1_tier_total',
                'traits_2_name',
                'traits_2_num_units',
    #            'traits_2_style',
    #            'traits_2_tier_current',
    #            'traits_2_tier_total',
                'traits_3_name',
                'traits_3_num_units',
    #            'traits_3_style',
    #            'traits_3_tier_current',
    #            'traits_3_tier_total',
                'traits_4_name',
                'traits_4_num_units',
    #            'traits_4_style',
    #            'traits_4_tier_current',
    #            'traits_4_tier_total',
                'traits_5_name',
                'traits_5_num_units',
    #            'traits_5_style',
    #            'traits_5_tier_current',
    #            'traits_5_tier_total',
                'traits_6_name',
                'traits_6_num_units',
    #            'traits_6_style',
    #            'traits_6_tier_current',
    #            'traits_6_tier_total',
                'traits_7_name',
                'traits_7_num_units',
    #            'traits_7_style',
    #            'traits_7_tier_current',
    #            'traits_7_tier_total',
                'traits_8_name',
                'traits_8_num_units',
    #            'traits_8_style',
    #            'traits_8_tier_current',
    #            'traits_8_tier_total',
                'traits_9_name',
                'traits_9_num_units',
    #            'traits_9_style',
    #            'traits_9_tier_current',
    #            'traits_9_tier_total',
                'traits_10_name',
                'traits_10_num_units',
    #            'traits_10_style',
    #            'traits_10_tier_current',
    #            'traits_10_tier_total',
    #            'units_0_character_id',
                'units_0_name',
                'units_0_rarity',
                'units_0_tier',
    #            'units_1_character_id',
                'units_1_itemNames_0',
                'units_1_name',
                'units_1_rarity',
                'units_1_tier',
    #            'units_2_character_id',
                'units_2_name',
                'units_2_rarity',
                'units_2_tier',
    #            'units_3_character_id',
                'units_3_name',
                'units_3_rarity',
                'units_3_tier',
    #            'units_4_character_id',
                'units_4_itemNames_0',
                'units_4_itemNames_1',
                'units_4_name',
                'units_4_rarity',
                'units_4_tier',
    #            'units_5_character_id',
                'units_5_itemNames_0',
                'units_5_itemNames_1',
                'units_5_name',
                'units_5_rarity',
                'units_5_tier',
    #            'units_6_character_id',
                'units_6_itemNames_0',
                'units_6_itemNames_1',
                'units_6_name',
                'units_6_rarity',
                'units_6_tier',
    #            'units_7_character_id',
                'units_7_itemNames_0',
                'units_7_itemNames_1',
                'units_7_itemNames_2',
                'units_7_name',
                'units_7_rarity',
                'units_7_tier',
    #            'units_8_character_id',
                'units_8_name',
                'units_8_rarity',
                'units_8_tier',
                'traits_11_name',
                'traits_11_num_units',
    #            'traits_11_style',
    #            'traits_11_tier_current',
    #            'traits_11_tier_total',
                'traits_12_name',
                'traits_12_num_units',
    #            'traits_12_style',
    #            'traits_12_tier_current',
    #            'traits_12_tier_total',
    #            'units_2_itemNames_0',
    #            'units_2_itemNames_1',
    #            'units_2_itemNames_2',
    #            'units_5_itemNames_2',
    #            'units_0_itemNames_0',
    #            'units_3_itemNames_0',
    #            'units_3_itemNames_1',
    #            'units_3_itemNames_2',
    #            'units_4_itemNames_2',
    #            'units_6_itemNames_2',
    #            'units_0_itemNames_1',
    #            'units_0_itemNames_2',
    #            'units_1_itemNames_1',
    #            'units_1_itemNames_2',
    #            'units_8_itemNames_0',
    #            'units_8_itemNames_1',
    #            'units_8_itemNames_2',
                'traits_13_name',
                'traits_13_num_units',
    #           'traits_13_style',
    #           'traits_13_tier_current',
    #           'traits_13_tier_total',
                'traits_14_name',
                'traits_14_num_units',
    #           'traits_14_style',
    #           'traits_14_tier_current',
    #           'traits_14_tier_total',
                'traits_15_name',
                'traits_15_num_units',
    #            'traits_15_style',
    #            'traits_15_tier_current',
    #            'traits_15_tier_total',
                'traits_16_name',
                'traits_16_num_units',
    #            'traits_16_style',
    #            'traits_16_tier_current',
    #            'traits_16_tier_total',
    #            'units_9_character_id',
                'units_9_itemNames_0',
                'units_9_itemNames_1',
                'units_9_itemNames_2',
                'units_9_name',
                'units_9_rarity',
                'units_9_tier',
                'units_9_items_0',
                'units_9_items_1',
                'units_9_items_2',
                'traits_17_name',
                'traits_17_num_units',
    #            'traits_17_style',
    #            'traits_17_tier_current',
    #            'traits_17_tier_total',
    #            'units_10_character_id',
                'units_10_itemNames_0',
                'units_10_itemNames_1',
                'units_10_itemNames_2',
                'units_10_name',
                'units_10_rarity',
                'units_10_tier',
                'units_10_items_0',
                'units_10_items_1',
                'units_10_items_2',
                'traits_18_name',
                'traits_18_num_units',
    #            'traits_18_style',
    #            'traits_18_tier_current',
    #            'traits_18_tier_total',
                'traits_19_name',
                'traits_19_num_units',
    #            'traits_19_style',
    #            'traits_19_tier_current',
    #            'traits_19_tier_total',
                'units_7_itemNames_3',
                'units_7_items_3'
                ]

unwanted_WITH_LIKE = ['_style', '_tier_current', '_tier_total', '_character_id', '_itemNames_']

# drop columns WITH words LIKE unwanted_WITH_LIKE
for column in merged_data:
    for keyword in unwanted_WITH_LIKE:
        if keyword in str(column):
            merged_data = merged_data.drop(str(column), axis = 'columns')

# drop some 'redundant' columns
redundant = ['companion_content_ID', 'companion_item_ID', 'companion_skin_ID', 'last_round', 'players_eliminated']
merged_data = merged_data.drop(redundant, axis = 'columns')

# Exploratory Questions
'''
1. What are the most picked augments at each stage? What are the least picked (but still picked) augments at each stage?
2. Which companion_species has the highest winrate?
3. What is the average level of players at the end of the game?
4. What is the most used trait?
5. Which puuid has the highest winrate?
6. Which augment has the highest winrate?
'''

# 1. What are the most picked augments at each stage?
augments = merged_data.iloc[:,0:3]
augments1 = augments['augments_0'].value_counts().to_frame()
augments2 = augments['augments_1'].value_counts().to_frame()
augments3 = augments['augments_2'].value_counts().to_frame()
print(augments1.head(20), '\n', augments2.head(20), '\n', augments3.head(20))

'''
1a. Some of the most picked augments at 2-1 include True Twos and Threes Company (very high tempo augments), Portable Forge
(which is fun), economy augments such as Trade Sector and Rich Get Richer, then augments that are give a consistent
passive buff such as the Vi Support, Ezreal Support, Annie Support, etc.
At 3-2 when most comps are probably cemented, Component Grab Bag is heavily picked to complete some items for tempo.
Supportive, consistent augments are still heavily picked.
At 4-2, damage is sought after with the Component Grab Bag and Jeweled Lotus picks, and notable Samira Support and
Soraka Support are picked heavily for AD and AP players respectively.
'''

print(augments1.tail(20), '\n', augments2.tail(20), '\n', augments3.tail(20))
'''
1b. Some of the losers at 2-1 are the Radiant Future Sight augment (since it requires a lot of thought most likely),
the Rammus Carry Augment, and the Senna Carry augment.
At 3-2, some notable low pick-rate augments include Preparation 3 (since you already have an established board),
the Sett and Zac carry augments (since they are "not good units" for carrying), and Big Friend 2 (usually a better
option is present if playing Brawlers, the only composition that can play this well).
At 4-2, some rarely picked augments are Tri Force 3 and 1 (usually only picked by people who are already playing many
reroll 3 cost units), Featherweights 2 and 3 (since at high elo, the average level is 8 and games are played around
4 cost carries), Velkoz Support (because the Velkoz unit is not very good), and Hacker and Mecha Prime emblems (not
much immediate value.)
'''