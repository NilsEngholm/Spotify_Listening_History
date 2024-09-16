import pandas as pd
import json
import sqlalchemy

jsonFile = 'main\\data\\test.json'


def jsonToDataframe(jsonFile):
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    df = pd.json_normalize(data)
    
    return df

rawdf = jsonToDataframe(jsonFile)
allColumns = rawdf.columns

df = rawdf[['track.name', 'played_at', 'track.id']]
print(df)