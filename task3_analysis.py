
import pandas as pd
import numpy as np

# Load the cleaned CSV file from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print the shape of the DataFrame
print("Loaded data:", df.shape)

# Display the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", average_score)
print("Average comments:", average_comments)

# Get score values as a NumPy array
scores = df["score"].to_numpy()

# Calculate statistics using NumPy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Find maximum and minimum scores
max_score = np.max(scores)
min_score = np.min(scores)

# Print NumPy statistics
print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)
print("Max score    :", max_score)
print("Min score    :", min_score)
# Count stories in each category
category_counts = df["category"].value_counts()

# Find the category with the most stories
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print("\nMost stories in:", top_category,
      f"({top_category_count} stories)")
# Find the story with the highest number of comments
most_commented = df.loc[df["num_comments"].idxmax()]

# Print its title and comment count
print("\nMost commented story:")
print("Title:", most_commented["title"])
print("Comments:", most_commented["num_comments"])
# Calculate engagement for each story
df["engagement"] = df["num_comments"] / (df["score"] + 1)

print("\nEngagement column added successfully.")
print(df[["title", "engagement"]].head())
# Mark stories as popular if their score is above average
df["is_popular"] = df["score"] > average_score

print("\nis_popular column added successfully.")
print(df[["title", "score", "is_popular"]].head())
# Save the analysed DataFrame for Task 4
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

# Print confirmation message
print(f"\nSaved {len(df)} rows to {output_file}")