import pandas as pd
import matplotlib.pyplot as plt

#Load the CSV
df = pd.read_csv('amazon_treadmills_final.csv')

#Cleaning/extracting prices, ratings and rating count

# Clean Rating: extract float number
df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)

# Clean Rating Count: remove commas and convert to int
df['Rating Count'] = df['Rating Count'].astype(str).str.replace(',', '', regex=False).astype(float)

# Clean Price: remove commas and convert to float
df['Price'] = df['Price'].astype(str).str.replace(',', '', regex=False).astype(float)

#Features to look for

features = {
    'foldable': ['foldable'],
    'incline': ['incline'],
    'under desk': ['under desk'],
    'compact': ['compact', 'small'],
    'pulse sensor': ['pulse sensor'],
    'remote control': ['remote control'],
    'quiet': ['quiet', 'low noise'],
    'bluetooth': ['bluetooth']
}

#Create boolean columns for each feature
for feature, keywords in features.items():
    pattern = '|'.join(keywords)
    df[feature] = df['Product Name'].str.lower().str.contains(pattern)

#Feautre popularity pie chart 

feature_counts = {feature: df[feature].sum() for feature in features}

plt.figure(figsize=(8,8))
plt.pie(feature_counts.values(), labels=[f.title() for f in feature_counts.keys()], autopct='%1.1f%%', startangle=140)
plt.title('Feature Popularity in Treadmill Listings')
plt.axis('equal')
plt.tight_layout()
plt.savefig("feature_popularity_pie.png")

#Weighted score by feature

weighted_scores = {
    feature: (df[df[feature]]['Rating'] * df[df[feature]]['Rating Count']).sum()
    for feature in features
}

plt.figure(figsize=(10,6))
plt.bar(weighted_scores.keys(), weighted_scores.values(), color='skyblue', edgecolor='black')
plt.title('Weighted Rating × Review Count by Feature')
plt.xlabel('Feature')
plt.ylabel('Weighted Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("weighted_scores_bar.png")

#Price histogram

price_bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
plt.figure(figsize=(10,6))
plt.hist(df['Price'], bins=price_bins, edgecolor='black', color='lightgreen')
plt.title('Treadmill Price Distribution')
plt.xlabel('Price ($)')
plt.ylabel('Number of Listings')
plt.xticks(price_bins, rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("price_distribution_histogram.png")

#Review count by price range

price_labels = [f"${price_bins[i]}–{price_bins[i+1]-1}" for i in range(len(price_bins)-1)]
df['Price Range'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels, include_lowest=True)

review_by_price = df.groupby('Price Range')['Rating Count'].sum()

plt.figure(figsize=(12,6))
review_by_price.plot(kind='bar', color='orange', edgecolor='black')
plt.title('Total Review Count per Price Range')
plt.xlabel('Price Range ($)')
plt.ylabel('Total Review Count')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
#Saving Chart as png
plt.savefig("review_count_by_price_range.png") 
