import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load cleaned CSV
df = pd.read_csv('amazon_treadmills_final.csv')

#Clean Rating and Rating Count
df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
df['Rating Count'] = df['Rating Count'].astype(str).str.replace(',', '', regex=False).astype(float)

#Define Features
features = {
    'foldable': ['foldable'],
    'incline': ['incline'],
    'under desk': ['under desk'],
    'compact/small': ['compact', 'small'],
    'pulse sensor': ['pulse sensor'],
    'remote control': ['remote control'],
    'quiet/low noise': ['quiet', 'low noise'],
    'bluetooth': ['bluetooth']
}

#Add Feature Columns
for feature, keywords in features.items():
    pattern = '|'.join(keywords)
    df[feature] = df['Product Name'].str.lower().str.contains(pattern)

#Calculate Popularity in Listings
feature_counts = {feature: df[feature].sum() for feature in features}

#Calculate Buyer Engagement (Weighted Popularity)
feature_weighted = {}
for feature in features:
    filtered = df[df[feature]]
    weighted = (filtered['Rating'] * filtered['Rating Count']).sum()
    feature_weighted[feature] = round(weighted, 2)

#Bar Chart: Side-by-Side Comparison
labels = list(features.keys())
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, list(feature_counts.values()), width, label='Feature Count in Listings')
bars2 = ax.bar(x + width/2, list(feature_weighted.values()), width, label='Buyer Engagement (Rating × Count)')

# Labels and Formatting
ax.set_ylabel('Frequency / Weighted Rating')
ax.set_title('Feature Popularity in Listings vs Actual Buyer Engagement')
ax.set_xticks(x)
ax.set_xticklabels([f.title() for f in labels], rotation=45, ha='right')
ax.legend()

#Annotate bar values
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{int(height)}' if height > 10 else f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # offset
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('feature_comparison.png')


