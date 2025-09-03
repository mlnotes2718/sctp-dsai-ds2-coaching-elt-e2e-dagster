import pandas as pd

df = pd.read_csv('austin_bikeshare_trips.csv', low_memory=False)

new_df = df.sample(n=300000, random_state=42)

new_df.to_csv('austin_bikeshare_trips_small.csv', index=False)

