import matplotlib.pylab as plt
import numpy as np
import pandas as pd
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

unwanted_WITH_LIKE = ['_style', '_tier_current', '_tier_total', '_itemNames_']

# drop columns WITH words LIKE unwanted_WITH_LIKE
for column in merged_data:
    for keyword in unwanted_WITH_LIKE:
        if keyword in str(column):
            merged_data = merged_data.drop(str(column), axis = 'columns')

# drop some 'redundant' columns
redundant = ['companion_content_ID', 'companion_item_ID', 'companion_skin_ID', 'last_round', 'players_eliminated']
merged_data = merged_data.drop(redundant, axis = 'columns')
merged_data = merged_data.reset_index(drop = True).copy()
merged_data = merged_data.replace('...._Augment_', '', regex = True)
merged_data.to_excel("tableau_data.xlsx")

# Exploratory Questions
'''
1. What are the most picked augments at each stage? What are the least picked (but still picked) augments at each stage?
2. Which companion_species has the highest winrate?
3. What is the average level of players at the end of the game?
4. What is the most used trait?
5. Which puuid has the highest winrate with at least 50 games played?
6. Which augment has the highest winrate?
'''

# 1. What are the most picked augments at each stage?
augments = merged_data.iloc[:,0:3]
augments1 = augments['augments_0'].value_counts().to_frame()
augments1.index = augments1.index.str.replace('...._Augment_', '', regex = True)
augments2 = augments['augments_1'].value_counts().to_frame()
augments2.index = augments2.index.str.replace('...._Augment_', '', regex = True)
augments3 = augments['augments_2'].value_counts().to_frame()
augments3.index = augments3.index.str.replace('...._Augment_', '', regex = True)

ax1 = augments1.head(20).plot(kind = 'bar', title = 'Most Picked 2-1 Augments')
ax1.set_xlabel('Augment')
ax1.set_ylabel('Count')

ax2 = augments2.head(20).plot(kind = 'bar', title = 'Most Picked 3-2 Augments')
ax2.set_xlabel('Augment')
ax2.set_ylabel('Count')

ax3 = augments3.head(20).plot(kind = 'bar', title = 'Most Picked 4-2 Augments')
ax3.set_xlabel('Augment')
ax3.set_ylabel('Count')


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
ax4 = augments1.tail(20).plot(kind = 'bar', title = 'Least Picked 2-1 Augments')
ax4.set_xlabel('Augment')
ax4.set_ylabel('Count')

ax5 = augments2.tail(20).plot(kind = 'bar', title = 'Least Picked 3-2 Augments')
ax5.set_xlabel('Augment')
ax5.set_ylabel('Count')

ax6 = augments3.tail(20).plot(kind = 'bar', title = 'Least Picked 4-2 Augments')
ax6.set_xlabel('Augment')
ax6.set_ylabel('Count')

'''
1b. Some of the least picked augments at 2-1 are the Radiant Future Sight augment (since it requires a lot of thought ), 
the Rammus Carry Augment, and the Senna Carry augment.
At 3-2, some notable low pick-rate augments include Preparation 3 (since you already have an established board),
the Sett and Zac carry augments (since they are "not good units" for carrying), and Big Friend 2 (usually a better
option is present if playing Brawlers, the only composition that can play this well).
At 4-2, some rarely picked augments are Tri Force 3 and 1 (usually only picked by people who are already playing many
reroll 3 cost units), Featherweights 2 and 3 (since at high elo, the average level is 8 and games are played around
4 cost carries), Velkoz Support (because the Velkoz unit is not very good), and Hacker and Mecha Prime emblems (not
much immediate value.)
'''

# 2. Which companion_species have the highest winrate?
print(merged_data.groupby('companion_species')['placement'].agg(['mean', 'count']).sort_values(by = 'mean', ascending = True))

#ax7 = merged_data.groupby('companion_species')['placement'].agg(['mean', 'count']).sort_values(by = 'mean', ascending = True)

'''
PetBuglet has the highest winrate at 3.67, followed by Chibi Ashe and Burno. The lowest winrate tacticians are
ElegantDragon, Chibi Ekko and Chibi Vi.
'''

# 3. What is the average player level at the end of the game?
print(merged_data['level'].mean())

ax8 = merged_data['level'].plot(kind = 'hist', title = 'Average Player Level')
ax8.set_xlabel('Level')

'''
It is roughly 7.976. The median is 8, and the mode is also 8.
'''

# 4. What are the most used traits? Least used traits?
trait_names = [column for column in merged_data.columns if 'traits' in column and 'name' in column]
trait_df = merged_data[trait_names].copy()
trait_df.apply(pd.Series.value_counts).sum(axis = 'columns').sort_values(ascending = False).plot(kind = 'bar')

'''
The top 10 most used traits are Aegis, Star Guardian, Mascot, Brawler, Threat, Ox Force, Underground, Prankster, Lasercorps,
and Channeler (aka Spellslinger).

The 10 least used traits for endgame boards are Forecaster, Supers, Arsenal, Recon, Civilian, Renegade, Admin, Mech Prime, 
Corrupted and Defender.
'''

# 5. Which puuid has the highest winrate with at least 50 games played?
merged_data.groupby('puuid')['placement'].agg(['mean', 'count']).sort_values(by = 'count', ascending = False).head(20) \
    .plot(kind = 'barh', y = 'mean', title = 'Average Placement')

'''
The player with puuid ending with PQA has a 3.227273 average placement over 66 games. This is actually ARaye,
the #1 player on the PH ladder. Another notable player has a 3.285714 average placement with puuid ending in
HsA. This is Sophti, another Challenger player.
'''

# 6. Which augment has the highest winrate? Lowest winrate?
augment_placements = pd.concat([merged_data.iloc[:,0:3], merged_data['placement']], axis = 'columns')
placements_1 = augment_placements[['augments_0', 'placement']]
placements_1.columns = placements_1.columns.str.replace('_0', '')
placements_2 = augment_placements[['augments_1', 'placement']]
placements_2.columns = placements_1.columns.str.replace('_1', '')
placements_3 = augment_placements[['augments_2', 'placement']]
placements_3.columns = placements_1.columns.str.replace('_2', '')
augment_averages = pd.concat([placements_1, placements_2, placements_3], axis = 'index').groupby('augments')['placement'] \
    .agg(['mean', 'count']).sort_values(by = 'mean', ascending = True)
augment_averages.index = augment_averages.index.str.replace('...._Augment_', '', regex = True)
augment_averages = augment_averages[augment_averages.index.str.contains("HyperRoll") == False]

augment_averages.head(20).plot(kind = 'bar', y = 'mean')
augment_averages.head(20).plot(kind = 'bar', y = 'count')

'''
Without caring about count, the highest winrate augment would be Preparation 3, picked once for a 1st place finish.
Caring about count, Slow and Steady, Star Guardian Emblem, Spellslinger Emblem, and Big Friend 2 all show a good top 4 rate.
'''

augment_averages.tail(20).plot(kind = 'bar', y = 'mean')
augment_averages.tail(20).plot(kind = 'bar', y = 'count')

'''
Some of the worst performing augments include Janna Carry, Leona Carry, Syndra Carry, Fiddlesticks Carry, Supers Soul, and
Preparation 3.
'''