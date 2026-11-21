
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed CSV file from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)

# Check the loaded data
print("Data loaded successfully!")
print("Shape:", df.shape)
print(df.head())

# Chart 1: Top 10 stories by score

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:47] + "..." if len(title) > 50 else title
)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(top_stories["short_title"], top_stories["score"])

# Show the highest score at the top
plt.gca().invert_yaxis()

# Add chart title and axis labels
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Adjust layout and save the chart
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")

# Display the chart
plt.show()

# Chart 2: Number of stories in each category

# Count stories in each category
category_counts = df["category"].value_counts()

# Create a bar chart with different colours
plt.figure(figsize=(9, 5))
plt.bar(
    category_counts.index,
    category_counts.values,
    color=["skyblue", "orange", "green", "red", "purple"]
)

# Add chart title and axis labels
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Adjust layout and save the chart
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")

# Display the chart
plt.show()

# Chart 3: Score vs Comments

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create a scatter plot
plt.figure(figsize=(9, 5))

# Plot non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="orange",
    label="Non-Popular"
)

# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    color="blue",
    label="Popular"
)

# Add chart title, axis labels and legend
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

# Adjust layout and save the chart
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")

# Display the chart
plt.show()

# Bonus: Combine all three charts into one dashboard

# Create a dashboard with 3 charts side by side
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Dashboard Chart 1: Top 10 stories
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")

# Dashboard Chart 2: Stories per category
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=["skyblue", "orange", "green", "red", "purple"]
)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Dashboard Chart 3: Score vs Comments
axes[2].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="orange",
    label="Non-Popular"
)
axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    color="blue",
    label="Popular"
)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Add the overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=18)

# Adjust spacing and save the dashboard
plt.tight_layout()
plt.savefig("outputs/dashboard.png")

# Display the dashboard
plt.show()
