from os.path import join, isfile
from pybaseball import statcast
import pandas as pd

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