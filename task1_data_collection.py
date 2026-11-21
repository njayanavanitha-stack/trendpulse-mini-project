import requests
import json
import time
from datetime import datetime
from pathlib import Path
# HackerNews API URLs
BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{BASE_URL}/topstories.json"

# Request header
headers = {"User-Agent": "TrendPulse/1.0"}
# Fetch the top 500 story IDs

# Fetch the top 500 story IDs safely
story_ids = []

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()
    story_ids = response.json()[:500]

    print(f"Successfully fetched {len(story_ids)} story IDs.")

except (requests.RequestException, ValueError) as error:
    print(f"Failed to fetch top story IDs: {error}")

    # Keywords used to identify each category
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}
# Identify the category based on title keywords
def get_category(title):
    title = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title:
                return category

    return None
# Fetch details of an individual HackerNews story
def fetch_story(story_id):

    story_url = f"{BASE_URL}/item/{story_id}.json"

    try:
        response = requests.get(
            story_url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        story = response.json()

        return story

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None
    # Store all successfully fetched stories
all_stories = []

# Fetch details for each story ID
for story_id in story_ids:

    story = fetch_story(story_id)

    if story and story.get("type") == "story" and story.get("title"):
        all_stories.append(story)

print(f"Successfully fetched {len(all_stories)} stories.")

# Fallback: fetch additional recent stories if top 500 produce fewer than 100
category_counts = {category: 0 for category in categories}

# Count the stories already available in each category
for story in all_stories:
    category = get_category(story.get("title", ""))

    if category and category_counts[category] < 25:
        category_counts[category] += 1

current_total = sum(category_counts.values())

if current_total < 100:
    print("\nFewer than 100 stories found. Checking recent stories...")

    try:
        extra_response = requests.get(
            f"{BASE_URL}/newstories.json",
            headers=headers,
            timeout=15
        )
        extra_response.raise_for_status()
        extra_story_ids = extra_response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch additional story IDs: {error}")
        extra_story_ids = []

    # Avoid fetching IDs already checked in the top 500
    existing_ids = set(story_ids)

    for extra_id in extra_story_ids:
        if current_total >= 100:
            break

        if extra_id in existing_ids:
            continue

        story = fetch_story(extra_id)

        if story and story.get("type") == "story" and story.get("title"):
            category = get_category(story["title"])

            if category and category_counts[category] < 25:
                all_stories.append(story)
                existing_ids.add(extra_id)
                category_counts[category] += 1
                current_total += 1

    print(f"Total matching stories after fallback: {current_total}")

# Store the final categorized stories
collected_stories = []

# Process each category
for category in categories:

    category_count = 0

    for story in all_stories:

        # Identify the category using the story title
        story_category = get_category(story["title"])

        if story_category == category and category_count < 25:

            collected_stories.append(story)
            category_count += 1

    print(f"{category}: {category_count} stories collected.")

    # Wait 2 seconds before processing the next category
    if category != list(categories.keys())[-1]:
        time.sleep(2)

print(f"\nTotal categorized stories: {len(collected_stories)}")
# Extract the required seven fields
final_stories = []

for story in collected_stories:

    story_data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": get_category(story.get("title", "")),
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().astimezone().isoformat()
    }

    final_stories.append(story_data)

print(f"Extracted {len(final_stories)} stories.")
# Create the data folder if it does not exist
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

# Create filename using today's date
today = datetime.now().strftime("%Y%m%d")
file_path = data_folder / f"trends_{today}.json"

# Save stories in JSON format
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(final_stories, file, indent=4, ensure_ascii=False)

print(f"Collected {len(final_stories)} stories.")
print(f"Saved to {file_path}")