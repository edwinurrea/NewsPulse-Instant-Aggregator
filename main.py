import feedparser
import time
import requests
from datetime import datetime
import pytz
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables from .env file
ntfy_topic = os.getenv("NTFY_TOPIC")
RSS_FEEDS = os.getenv("RSS_FEEDS")

if RSS_FEEDS:
    RSS_FEEDS = [url.strip() for url in RSS_FEEDS.split(",")]
else:
    # Default RSS feeds if not provided in .env
    RSS_FEEDS = [] # Insert feed links here

CHECK_INTERVAL = 30 # Checks Every 30 Seconds
seen_articles = set() # Stores Seen Articles/Stores Unique Elements

def format_description(description):
    synopsis_match = re.search(r'<p>(.*?)<\/p>', description, re.DOTALL)
    synopsis = synopsis_match.group(1) if synopsis_match else ""

    provider_match = re.search(r'<a [^>]+>([^<]+)</a>\.', description)
    provider = provider_match.group(1) if provider_match else ""

    return synopsis, provider

def format_published_date(published):
    # Convert published date to datetime object
    published = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")

    # Convert from UTC timezone to EST
    timezone = pytz.timezone("America/New_York")
    published = published.astimezone(timezone) 

    # Format the published date to a more readable format
    published = published.strftime("%B %d, %Y %I:%M:%S %p %Z")
    print(f"Published Date: {published}")
    return published

def fetch_latest_news():
    # Fetch new articles from RSS feeds. 
    print("Fetching latest news...")
    for feed_url in RSS_FEEDS:
        print("Fetching articles from:", feed_url)
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            print(f"No new articles found from {feed_url}.")
            continue

        for entry in feed.entries:
            print(f"Article Found: {entry.title}")
            if entry.link not in seen_articles:
                print("New Article Detected:", entry.title)
                seen_articles.add(entry.link)
                send_notification(entry.title, entry.link, entry.description, entry.published)

def send_notification(title, url, description, published):
    # Sends Notification using ntfy.sh To iOS, Instantaneously.
    print("Sending notification...")
    ntfy_url = f"https://ntfy.sh/{ntfy_topic}"

    # Format the description and published date
    synopsis = format_description(description)[0]
    provider = format_description(description)[1]
    published = format_published_date(published)
    print("p:" + provider)

    data = synopsis + "\n" + published

    title = provider + ": " + title

    headers = {
        "Title": title,
        "Click": url,
        "Priority": "high",
        "Tags": "warning",
        "Actions": f"view, View Article, {url}",
    }

    try:
        response = requests.post(ntfy_url, data=data, headers=headers)
        print(f"Response: {response.status_code}")

        if response.status_code == 200:
            print(f"Notification sent! Titled: {title}")
        else:
            print(f"Failed to send notification. Status code: {response.status_code} Response Text: {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    # Main Loop Runs Indefinitely
    print("Starting Newsfeed Checker...")
    while True:
        fetch_latest_news()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()