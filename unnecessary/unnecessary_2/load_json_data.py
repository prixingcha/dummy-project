import json

# Path to the JSON file
file_path = 'output.json'

# Load JSON data from file
with open(file_path, 'r') as file:
    data = json.load(file)

# Access elements
print("Total Results:", data["pageInfo"]["totalResults"])
print("Results Per Page:", data["pageInfo"]["resultsPerPage"])

for item in data["items"]:
    print("\nChannel Title:", item["snippet"]["title"])
    print("Description:", item["snippet"]["description"])
    print("Custom URL:", item["snippet"].get("customUrl", ""))
    print("Published At:", item["snippet"]["publishedAt"])
    print("Country:", item["snippet"].get("country", ""))
    print("View Count:", item["statistics"]["viewCount"])
    print("Subscriber Count:", item["statistics"]["subscriberCount"])
    print("Hidden Subscriber Count:", item["statistics"].get("hiddenSubscriberCount", ""))
    print("Video Count:", item["statistics"]["videoCount"])
    print("Topic IDs:", item["topicDetails"].get("topicIds", ""))
    print("Topic Categories:", item["topicDetails"].get("topicCategories", ""))
    print("Privacy Status:", item["status"]["privacyStatus"])
    print("Is Linked:", item["status"]["isLinked"])
    print("Long Uploads Status:", item["status"].get("longUploadsStatus", ""))
    print("Made For Kids:", item["status"]["madeForKids"])
    print("Keywords:", item["brandingSettings"]["channel"].get("keywords", ""))
