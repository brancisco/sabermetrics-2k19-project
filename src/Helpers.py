from os.path import join, isfile
from pybaseball import statcast
import pandas as pd
import numpy as np

def get_player_map(unique_ids, infile):
  # needs to remove players who did not play in 2018
  df = pd.read_csv(infile, encoding='latin-1')
  player_map = {}

  for row in df.iterrows():
    row = row[1]
    mlb_id = int(float(row.mlb_id))
    if mlb_id in unique_ids:
      player_map[mlb_id] = row.mlb_name

  class PMap:
    def __init__(self, pm):
      self.map = pm
    def get(self, pid):
      if pid in self.map:
        return self.map[pid]
      else:
        return str(pid)
    def getadd(self, pid):
      if pid in self.map:
        return self.map[pid]
      else:
        self.map[pid] = str(pid)
        return str(pid)

  return PMap(player_map)

def get_statcast_data(directory, year):
  year = str(year)
  data_path = join(directory, 'statcast_data_{}.csv'.format(year))
  sc_data = None
  if not isfile(data_path):
    date_ranges = [
      ('$-01-01', '$-03-31'),
      ('2018-04-01', '$-06-30'),
      ('$-07-01', '$-09-30'),
      ('$-10-01', '$-12-31')
    ]
    date_ranges = [(date[0].replace('$', year), date[1].replace('$', year)) for date in date_ranges]
    data = []
    for dr in date_ranges:
      data.append(statcast(start_dt=dr[0], end_dt=dr[1]))
    sc_data = pd.concat(data, ignore_index=True)
    sc_data.to_csv(data_path)
  else:
    sc_data = pd.read_csv(data_path, index_col=0)
  return sc_data.copy()

def event_map(e):
  """
  Map a string from the statcast database events column to a key
  @param e str which is a value from the events column
  @return str|int (h, hr, k) | -1
  """
  emap = {
    'single': 'h',
    'double': 'h',
    'triple': 'h',
    'home_run': 'hr',
    'strikeout': 'k'
  }
  if e in emap:
    return emap[e]
  else:
    return -1

def get_proba_function(df):
  """
  Create a function which produces the probability of: a hit (excluding homerun), homerun, and strike
  @param df pandas.DataFrame which has a years seasons worth of statcast data
  @return a function which takes in an event (h, hr, k), and returns a probability of the event
  """
  n_1b = len(df.loc[df.events == 'single'])
  n_2b = len(df.loc[df.events == 'double'])
  n_3b = len(df.loc[df.events == 'triple'])
  n_hr = len(df.loc[df.events == 'home_run'])
  n_so = len(df.loc[df.events == 'strikeout'])
  n_bb = len(df.loc[df.events == 'walk'])
  emap = { 'h': n_1b + n_2b + n_3b, 'hr': n_hr, 'k': n_so }
  return lambda e: emap[e] / sum(list(emap.values()))

def wager(p, b, k):
  """
  Calculates the points a pitcher, and a batter should wager on a given event
  @param p float: score of pitcher
  @param b float: score of batter
  @param k int: wager factor, weights how much players should wager
  @return touple (float, float): (pitchers wager, batters wager)
  """
  ep = (10**(p/400))/((10**(p/400)) + (10**(b/400)))
  eb = 1-ep
  return (round(k(p)*ep, 3), round(k(b)*eb, 3))

def get_assign_points_function(pf):
  """
  @param pf float: probability function of an event
  @return function which takes (p, b, e, f) as args
  """
  def assign_points_function(p, b, e, k):
    """
    @param p float: score of pitcher
    @param b float: score of batter
    @param e str[] | str: event (h | hr | k)
    @param k int: wager factor, weights how much players should wager
    @return tuple (float, float) which contains (pitchers new points, batters new points)
    """
    pw, bw = wager(p, b, k)
    if type(e) == str:
      event = e
    else:
      event = e.pop(0)
    proba = pf(event)
    points = (None, None)
    if event == 'k':
      percent = 1 - (proba)
      points = (p+(bw*percent), b-(bw*percent))
    elif event == 'h':
      percent = (1 - (pf('h') + pf('hr')))/(pf('h')/pf('hr'))
      points = (p-(bw*percent), b+(bw*percent))
    elif event == 'hr':
      percent = (1 - (pf('h') + pf('hr')))*(pf('h')/pf('hr'))
      points = (p-(bw*percent), b+(bw*percent))
    points = (round(points[0], 3), round(points[1], 3))
    if type(e) == str or len(e) == 0:
      return points
    else:
      return assign_points_function(points[0], points[1], e, f)
  return assign_points_function

def k_function(p):
  """
  @param p float which is the number of points a player has
  @ return float which is the k multiplier for how much a player should wager
  """
  res = np.exp(3600/(p))
  if res >= 20:
    return 20*2
  elif res <= 10:
    return 10*2
  else:
    return res*2

def history_avg(arr, n):
  """
  @param arr list which contains floats 
  @param n int specifying how far back to average (window)
  @return average from window length n to end of arr
  """
  l = len(arr)
  if n > l:
    n = l
  return np.mean(arr[-n:])
