import pandas as pd
import sys
# Get the name of the json file
filename = sys.argv[1]
#
# At first I got ValueError: Trailing data. I added lines=True.
df = pd.read_json(filename+'.json', lines=True)
# TBD: Columns to drop... basically all columns that arent Pr, Pa, I...Make this more robust...
df.drop(['_id'], axis=1, inplace=True)
df = df.set_index('timestamp')
# Set the time to PST
df.index = df.index.tz_localize('UTC').tz_convert('US/Pacific')
df_pickled = df.to_pickle(filename+'.pkl')
