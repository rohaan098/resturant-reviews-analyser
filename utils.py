import re
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Placeholder for getting reviews from Google
def get_google_reviews(restaurant_name):
    # Replace with real integration using Places API or scraping if needed
    return [
        "The pizza was amazing and service was excellent!",
        "Very slow service. Food was cold and tasteless.",
        "Loved the ambiance and the staff was very polite.",
        "Not worth the price. Poor hygiene.",
        "Delicious pasta and great customer service."
    ]

# NLP to extract meaningful key phrases from reviews
def extract_key_phrases(reviews):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=50)
    X = vectorizer.fit_transform(reviews)
    keywords = vectorizer.get_feature_names_out()
    return keywords.tolist()