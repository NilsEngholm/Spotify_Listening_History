import pandas as pd
import json

jsonFile = 'main\\data\\test.json'


def jsonToDataframe(jsonFile):
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    df = pd.json_normalize(data)
    
    return df

df = jsonToDataframe(jsonFile)
songNames = df['track.name']
timePlayed = df['played_at']
print(f"{songNames} {timePlayed}")