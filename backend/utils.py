import requests
from keybert import KeyBERT

kw_model = KeyBERT()

def autocomplete_search(api_key, input_text):
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        "input": input_text,
        "types": "establishment",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def get_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,reviews,rating",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def extract_top_and_bottom_reviews(reviews, top_n=10):
    sorted_reviews = sorted(reviews, key=lambda x: x.get('rating', 0), reverse=True)
    top_reviews = sorted_reviews[:top_n]
    bottom_reviews = sorted_reviews[-top_n:]
    return top_reviews, bottom_reviews

def extract_key_phrases_from_reviews(reviews):
    texts = [review['text'] for review in reviews if 'text' in review]
    combined_text = " ".join(texts)
    if not combined_text:
        return []
    keywords = kw_model.extract_keywords(combined_text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    return [kw for kw, _ in keywords]