import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
data = pd.read_csv("https://raw.githubusercontent.com/datasets/player-performance-in-english-premier-league/main/data/performance.csv")

# Filter the data to show only the columns we need
data = data[['Name', 'Club', 'Position', 'Minutes Played', 'Goals']]

# Group the data by club and sum the minutes played and goals
grouped = data.groupby('Club').sum()

# Plot the data as a bar chart
grouped.plot(kind='bar', x='Club', y='Goals')
plt.xlabel("Club")
plt.ylabel("Goals Scored")
plt.title("Total Goals Scored by Club in Premier League")
plt.show()