import requests
from sklearn.feature_extraction.text import TfidfVectorizer

def get_autocomplete_suggestions(query, api_key=None):
    if not api_key:
        api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return []

    try:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": query,
            "types": "establishment",  # Limits to businesses
            "key": api_key
        }
        response = requests.get(url, params=params).json()
        predictions = response.get("predictions", [])
        return [p["description"] for p in predictions]
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return []
def get_google_reviews(restaurant_name, api_key):
    # 1. Find place_id for the restaurant
    search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    search_params = {
        'query': restaurant_name,
        'key': api_key
    }
    search_resp = requests.get(search_url, params=search_params).json()
    if not search_resp.get('results'):
        return []

    place_id = search_resp['results'][0]['place_id']

    # 2. Get place details with reviews
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    details_params = {
        'place_id': place_id,
        'fields': 'review',
        'key': api_key
    }
    details_resp = requests.get(details_url, params=details_params).json()
    reviews = details_resp.get('result', {}).get('reviews', [])

    return [r['text'] for r in reviews if 'text' in r]

def extract_key_phrases(reviews):
    if not reviews:
        return []
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=30)
    X = vectorizer.fit_transform(reviews)
    phrases = vectorizer.get_feature_names_out()
    return phrases.tolist()
