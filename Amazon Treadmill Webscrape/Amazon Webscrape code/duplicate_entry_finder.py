import pandas as pd

#Load combined listings from regular treadmills and walking pads
df = pd.read_csv('amazon_treadmills_clean.csv')

#Check for fully identical rows (same name, rating, rating count, price)
full_duplicates = df[df.duplicated(keep=False)]

print(f"Found {full_duplicates.shape[0]} full duplicate rows.")
print(full_duplicates)

#Drop full duplicates
df_cleaned = df.drop_duplicates()

#Save the clean version
df_cleaned.to_csv('amazon_treadmills_final.csv', index=False)

print(f"Final dataset has {df_cleaned.shape[0]} rows after removing full duplicates.")
