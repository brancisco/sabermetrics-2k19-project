import json
import pandas as pd
from os.path import join

def main():
  data = '../data'
  file = 'master.csv'
  df = pd.read_csv(join(data, file), encoding='latin-1')
  player_map = {}

  for row in df.iterrows():
    row = row[1]
    player_map[row.mlb_name] = row.mlb_id

  with open('../docs/data/player_map.json', 'w') as file:
    json.dump(player_map, file)

if __name__ == '__main__':
  main()