import pandas as pd

df = pd.read_csv('bikeshare_trips.csv')

new_df = df.sample(n=300000, random_state=42)

new_df.to_csv('bikeshare_trips_small.csv', index=False)

