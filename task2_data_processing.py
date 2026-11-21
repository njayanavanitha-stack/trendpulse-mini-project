
import pandas as pd
from pathlib import Path

# Find the JSON file created by Task 1
data_folder = Path("data")
json_files = sorted(data_folder.glob("trends_*.json"))

# Check whether the JSON file exists
if not json_files:
    print("No Task 1 JSON file found in the data folder.")
else:
    json_file = json_files[-1]

    # Load JSON data into a Pandas DataFrame
    df = pd.read_json(json_file)

    # Print the number of rows loaded
    print(f"Loaded {len(df)} stories from {json_file}")
        # Remove duplicate stories using post_id
    df = df.drop_duplicates(subset="post_id")

    # Print rows remaining after removing duplicates
    print(f"After removing duplicates: {len(df)}")
    # Remove rows with missing required values
    df = df.dropna(subset=["post_id", "title", "score"])

    # Print rows remaining after removing missing values
    print(f"After removing nulls: {len(df)}")
        # Convert score and num_comments into integer data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    print("Data types converted successfully.")
    print(df[["score", "num_comments"]].dtypes)
    # Remove stories with a score below 5
    df = df[df["score"] >= 5]

    # Print rows remaining after removing low scores
    print(f"After removing low scores: {len(df)}")
        # Remove extra spaces from story titles
    df["title"] = df["title"].str.strip()

    print("Extra spaces removed from titles.")
        # Save the cleaned DataFrame as a CSV file
    csv_file = data_folder / "trends_clean.csv"
    df.to_csv(csv_file, index=False)

    # Print the number of rows saved
    print(f"\nSaved {len(df)} rows to {csv_file}")

    # Display the number of stories in each category
    print("\nStories per category:")
    print(df["category"].value_counts().to_string())
