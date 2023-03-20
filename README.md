# PH Teamfight Tactics Data Analysis

## TL;DR

An ETL pipeline was built to get match data of PH Challenger/GM+ players for the game Teamfight Tactics using the Riot Developer API. The data is then preprocessed into .csv files and analyzed with data analysis techniques. Afterwards, a model is trained to try and predict where a certain combination of units/traits/items would place if played in-game.

## Code and Resources Used

- Python Version: 3.10
- Packages: numpy, pandas, requests, sklearn, flatten_json
- Riot Developer API: https://developer.riotgames.com/apis

## To Do List

- [x] Extract Match Data using Riot Developer API
- [x] Create ETL Pipeline to automatically preprocess and write to .csv
- [ ] Perform Exploratory Data Analysis
- [ ] Create Tableau Dashboard for Match Analysis
- [ ] Choose and Train Model for Placement Predictor
- [ ] Finish README 