import json
import pandas as pd
import numpy as np
from os.path import join
from Helpers import *
from tqdm import tqdm
import sys

cmap = {
  'y': '#fef160',
  'g': '#2ecc71',
  'b': '#22a7f0',
  'r': '#f62459',
}
  
e_style = {
  'p': {
    'k': 'point {{ fill-color: {} }}'.format(cmap['g']),
    'h': 'point {{ fill-color: {} }}'.format(cmap['y']),
    'hr': 'point {{ fill-color: {} }}'.format(cmap['r'])
  },
  'b': {
    'k': 'point {{ fill-color: {} }}'.format(cmap['r']),
    'h': 'point {{ fill-color: {} }}'.format(cmap['b']),
    'hr': 'point {{ fill-color: {} }}'.format(cmap['g'])
  }
}

def event_style(e, pb):
  return e_style[pb][e]

def export_mjs_module(outfile, data):
  out = 'export default ' + json.dumps(data)
  with open(outfile, 'w') as file:
    file.write(out)

def create_player_data(data_folder, out_folder, year):
  print('loading data...')
  data = get_statcast_data(data_folder, year)
  print('finished loading data...')
  # factor to weight how much points should be wagered in an event
  wf = k_function
  # event probability function
  epf = get_proba_function(data)
  # assign points function
  update_score = get_assign_points_function(epf)
  # history: how far back to avg a score (prevents sensitivity to local events)
  h = 5

  unique_ids = list(map(int, list(set(list(data.pitcher.unique()) + list(data.batter.unique())))))
  player_map = get_player_map(unique_ids, join(data_folder, 'master.csv'))

  point_df = data.loc[:, ('game_date', 'game_pk', 'sv_id', 'pitcher', 'batter', 'events')].copy()
  points_df = point_df.sort_values(['game_date', 'sv_id'])
  # index, ranking, event_type/against, style
  pitchers_cdata = { int(p): [[0, 1500.0, 'Initialized', 'point {fill-color: #00FF00}']]
              for p in point_df.pitcher.unique()}
  batters_cdata = { int(b): [[0, 1500.0, 'Initialized', 'point {fill-color: #00FF00}']]
             for b in point_df.batter.unique()}
  pitchers = { int(p): [1500.0]
              for p in point_df.pitcher.unique()}
  batters = { int(b): [1500.0]
             for b in point_df.batter.unique()}

  for row in tqdm(point_df.iterrows()):
    row = row[1]
    event = event_map(row.events)
    if event != -1:
      p_id = int(row.pitcher)
      b_id = int(row.batter)
      update = update_score(history_avg(pitchers[p_id], h), history_avg(batters[b_id], h), event, wf)
      if p_id not in unique_ids:
        print('p_id: ', p_id)
      if b_id not in unique_ids:
        print('b_id: ', b_id)
      pitchers_cdata[p_id].append([
        len(pitchers_cdata[p_id]),
        update[0],
        row.events + '\nAgainst: ' + player_map.getadd(b_id),
        event_style(event, 'p')
      ])
      batters_cdata[b_id].append([
        len(batters_cdata[b_id]),
        update[1],
        row.events + '\nAgainst: ' + player_map.getadd(p_id),
        event_style(event, 'b')
      ])
      pitchers[p_id].append(update[0])
      batters[b_id].append(update[1])

  export_mjs_module(join(out_folder, 'batters-{}.mjs'.format(year)), batters_cdata)
  export_mjs_module(join(out_folder, 'pitchers-{}.mjs'.format(year)), pitchers_cdata)
  export_mjs_module(join(out_folder, 'player-map-{}.mjs'.format(year)), player_map.map)

def main():
  if len(sys.argv) < 2:
    print('usage: python3 create_app_data.py int:year')
    exit(1)
  year = 0
  try:
    year = int(float(sys.argv[1]))
  except:
    print('usage: python3 create_app_data.py int:year')
    exit(1)

  create_player_data('../data', '../docs/data', year)

if __name__ == '__main__':
  main()