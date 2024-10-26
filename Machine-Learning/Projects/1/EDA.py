import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from pandas.plotting import scatter_matrix

df = pd.read_csv('spotify.csv')

# Understanding the Data
print(df.head()) #gives first 5 rows data (i can also mention head(10) if i want 10 rows) 
print(df.info()) # gives content in the data i.e what each coloumn is representing
print(df.describe()) #This gives mean,count and other mathematical parameters for the eacch coloumn data

print(pd.isnull(df).sum())

# Top 10 popular songs
sorted_df=df.sort_values('popularity',ascending=False).head(10)
print(sorted_df)

# List of numeric features to explore
numeric_features = df.select_dtypes(include=['float64', 'int64']).columns

num_features = len(numeric_features)
cols = 5
rows = (num_features + cols - 1) // cols 

# Plotting histograms
plt.figure(figsize=(15, 8))
for i, feature in enumerate(numeric_features, start=1):
    plt.subplot(rows, cols, i)
    sns.histplot(df[feature], kde=True)
    plt.title(f'Distribution of {feature}')
plt.tight_layout()
plt.show()

# Plotting box plots
plt.figure(figsize=(15, 8))
for i, feature in enumerate(numeric_features, start=1):
    plt.subplot(rows, cols, i)
    sns.boxplot(x=df[feature])
    plt.title(f'Boxplot of {feature}')
plt.tight_layout()
plt.show()

# Plotting violin plots
plt.figure(figsize=(15, 7))
for i, feature in enumerate(numeric_features, start=1):
    plt.subplot(rows, cols, i)
    sns.violinplot(x=df[feature])
    plt.title(f'Violin plot of {feature}')
plt.tight_layout()
plt.show()

# Encoding categorical columns
df['artists_enc'] = df['artists'].astype('category').cat.codes
df['album_name_enc'] = df['album_name'].astype('category').cat.codes
df['track_name_enc'] = df['track_name'].astype('category').cat.codes
df['genre_enc'] = df['track_genre'].astype('category').cat.codes
df_numeric = df.select_dtypes(include=['float64', 'int64', 'int32'])

df_numeric['artists_enc'] = df['artists_enc']
df_numeric['album_name_enc'] = df['album_name_enc']
df_numeric['track_name_enc'] = df['track_name_enc']
df_numeric['genre_enc'] = df['genre_enc']
corr_df = df_numeric.corr(method="pearson")
plt.figure(figsize=(14, 10))
heatmap = sns.heatmap(corr_df, annot=True, fmt=".1g", vmin=-1, vmax=1, center=0, cmap="inferno", linewidths=1, linecolor="Black")
heatmap.set_title("Correlation Heatmap Including Encoded Features")
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)
plt.show()

#sampling data
sample_df=df.sample(int(0.004*len(df)))
print(len(sample_df))

# Now creating regression plot between loudness and energy as in heat map they have more correlation:
# incresing plot is coming
plt.figure(figsize=(10,6))
sns.regplot(data=sample_df,y="loudness",x="energy",color="b").set(title="Loudness vs energy correlation plot")
plt.show()
# energy vs accousticness
plt.figure(figsize=(10,6))
sns.regplot(data=sample_df,y="energy",x="acousticness",color="c").set(title="energy vs acousticness correlation plot")
plt.show()

unique_genres_count = df['track_genre'].nunique()
print(f"There are {unique_genres_count} different genres in the dataset.")

# duration vs track_genre
plt.figure(figsize=(15, 8))
plt.title("Songs Duration in Different Genres")
colors = sns.color_palette("husl", df['track_genre'].nunique())
sns.barplot(y='duration_ms', x='track_genre', hue='track_genre', data=df, palette=colors, errorbar=None, dodge=False)
plt.xlabel("Genres",labelpad=10)
plt.ylabel('Duration in ms',labelpad=10)
plt.xticks(rotation=90)
plt.legend([],[], frameon=False) 
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2) 
plt.tight_layout(pad=3.0)
plt.show()

# popularity vs track_genre
sns.set_style(style="darkgrid")
famous = df.sort_values("popularity", ascending=False)
unique_genres = famous.head(10)['track_genre'].unique()
colors = sns.color_palette("viridis", len(unique_genres))
sns.barplot(y='track_genre', x='popularity', data=famous.head(10), palette=colors, hue='track_genre', dodge=False)
plt.title("Top Genres by Popularity")
plt.show()

# Plotting for categorical data
unique_track_ids = df['track_id'].nunique()
print(f"Unique track IDs: {unique_track_ids}")

unique_artists = df['artists'].nunique()
print(f"Unique artists: {unique_artists}")

unique_album_names = df['album_name'].nunique()
print(f"Unique album names: {unique_album_names}")

unique_track_names = df['track_name'].nunique()
print(f"Unique track names: {unique_track_names}")

unique_track_genres = df['track_genre'].nunique()
print(f"Unique track genres: {unique_track_genres}")

unique_explicit = df['explicit'].nunique()
print(f"Unique values in explicit: {unique_explicit}")



plt.figure(figsize=(10, 10))

gs = gridspec.GridSpec(3, 2, height_ratios=[1, 0.5, 1])
# Below i have shown only head(10) as all cannot be displayed properly and is looking clumsy
# 1.artists
plt.subplot(gs[0, 0])  
artists = df['artists'].value_counts().head(10)
artists.plot(kind='bar', color='orange')
plt.title('Artists')
plt.xlabel('Artist')
plt.ylabel('Number of Tracks')
plt.xticks(rotation=45)

# 2.album_name
plt.subplot(gs[0, 1]) 
albums = df['album_name'].value_counts().head(10)
albums.plot(kind='bar', color='blue')
plt.title('Albums')
plt.xlabel('Album Name')
plt.ylabel('Number of Tracks')
plt.xticks(rotation=45)

# 3.track_name
plt.subplot(gs[1, :])  
track_names = df['track_name'].value_counts().head(10)
track_names.plot(kind='bar', color='red')
plt.title('Track Names')
plt.xlabel('Track Name')
plt.ylabel('Number of Occurrences')
plt.xticks(rotation=45)

# 4.track_genre
plt.subplot(gs[2, 0]) 
genres = df['track_genre'].value_counts().head(10)
genres.plot(kind='bar', color='green')
plt.title('Track Genres')
plt.xlabel('Genre')
plt.ylabel('Number of Tracks')
plt.xticks(rotation=45)

# 5.explicit
plt.subplot(gs[2, 1]) 
df['explicit'].value_counts().plot(kind='bar', color=['purple', 'pink'])
plt.title('Distribution of Explicit Content')
plt.xlabel('Explicit')
plt.ylabel('Number of Tracks')
plt.xticks([0, 1], ['False', 'True'], rotation=0)

plt.tight_layout()

plt.show()





