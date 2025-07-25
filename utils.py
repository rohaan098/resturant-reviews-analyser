import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def get_place_id(restaurant_name):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": restaurant_name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("candidates"):
        return data["candidates"][0]["place_id"]
    return None

def get_google_reviews(restaurant_name):
    place_id = get_place_id(restaurant_name)
    if not place_id:
        return []

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "reviews",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(details_url, params=params)
    data = response.json()

    reviews = []
    for review in data.get("result", {}).get("reviews", []):
        reviews.append(review.get("text", ""))
    return reviews

# NLP to extract meaningful key phrases from reviews
def extract_key_phrases(reviews):
    if not reviews:
        return []

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=50)
    X = vectorizer.fit_transform(reviews)
    keywords = vectorizer.get_feature_names_out()
    return keywords.tolist()

if __name__ == "__main__":
    restaurant = input("Enter restaurant name: ")
    reviews = get_google_reviews(restaurant)
    if not reviews:
        print("No reviews found.")
    else:
        phrases = extract_key_phrases(reviews)
        print("Key Phrases:", phrases)
