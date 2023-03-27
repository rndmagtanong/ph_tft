# PH Teamfight Tactics Data Analysis

## TL;DR

An ETL pipeline was built to get match data of PH Challenger/GM+ players for the game Teamfight Tactics (hereafter TFT) using the Riot Developer API. The data is then preprocessed into .csv files and analyzed with data analysis techniques. Afterwards, a model is trained to  predict where a certain combination of units/traits/items would place if played in-game.

## Code and Resources Used

- Python Version: 3.10
- Packages: matplotlib, numpy, pandas, re, requests, seaborn, sklearn, flatten_json
- Riot Developer API: https://developer.riotgames.com/apis

## To Do List

- [x] Extract Match Data using Riot Developer API
- [x] Create ETL Pipeline to automatically preprocess and write to .csv
- [x] Perform Exploratory Data Analysis
- [x] Choose and Train Model for Placement Predictor
- [ ] Finish README 

## Data Collection

The data used was collected on March 16, 2023, during the Set 8 period of the game TFT by Riot Games. Developer access was requested and granted, then the `requests` library was used to first identify the best players of the region, then get their names, then their player universally unique IDentifiers, and finally the last 50 matches that they each had played.

Since this process could and should be done repeatedly, a pipeline was created using `sklearn.pipeline` to drop matches played in the non-ranked game modes. Some preprocessing is also done at this step including dropping full NaN columns, deleting columns that contain 'garbage' data, resetting the index, and describing the amount of missing data (which there should be a lot of considering the high dimensionality of TFT). This iteration is then saved to a *.csv* file for data analysis.

From here, another pipeline is used to created the dataset for the machine learning model. This pipeline deletes columns with cosmetic features that do not affect the result of the game, and columns that have only 10% of its data filled. 

All this can then be done by adding a valid Riot Developer API key then running the script. The output will be four *.csv* files, containing match data of the best players in the PH region.

## Exploratory Data Analysis

With the data collected, it's time to glean insight from them. Some interesting questions to ask are:

1. What are the most picked augments at each stage?
2. What are the least picked (but still picked) augments at each stage?
3. Which companion_species has the highest winrate?
4. What is the most used trait?
5. Which puuid has the highest winrate with at least 50 games played?
6. Which augment has the highest winrate?

### Most Picked Augments

### Least Picked Augments

### Species Placement

### Most Used Trait

### Highest WR Player

### Highest WR Augment
