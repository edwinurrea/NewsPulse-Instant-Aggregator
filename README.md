# NewsPulse-Instant-Aggregator
An AI-powered news classifier that detects and alerts critical real-world events instantly from RSS feeds using a custom-trained model.

# Critical News Classifion 🔥📰

This project is a machine learning-powered system that monitors real-world news and identifies **high-importance events** like government actions, crises, or policy changes. Built using scikit-learn and TF-IDF, it classifies news headlines and descriptions based on their criticality and sends push notifications when necessary.

## 💡 Features
- Trains on labeled news data (e.g., fake-and-real-news dataset)
- Currently classifies headlines as "critical" (1) or "not critical" (0)
- Supports RSS feed monitoring
- Push notifications (focused on iOS) via ntfy.sh
- Lightweight and fast (TF-IDF + Random Forest)

## 🧠 Model
- TF-IDF Vectorizer
- RandomForestClassifier from Scikit-learn

## 📦 Setup
Currently in progress, and will be finalized when the project is done.
For now, make sure the ntfy_topic is how you want it, a code that only you would use; ntfy_topic = "your-custom-topic-name".
Add your RSS feeds; RSS_FEEDS = [].
Then, run the script.
(The feed notification is currently formatted very nicely, but not under control just yet.)
