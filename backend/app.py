from flask import Flask, request, jsonify
from utils import autocomplete_search, get_place_details, extract_top_and_bottom_reviews, extract_key_phrases_from_reviews
import os

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/")
def index():
    return {"status": "Service running"}

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400
    data = autocomplete_search(GOOGLE_API_KEY, query)
    suggestions = [item['description'] for item in data.get('predictions', [])]
    return jsonify({"suggestions": suggestions})

@app.route("/reviews", methods=["GET"])
def reviews():
    place_id = request.args.get("place_id", "")
    if not place_id:
        return jsonify({"error": "Missing 'place_id' parameter"}), 400
    details = get_place_details(GOOGLE_API_KEY, place_id)
    result = details.get("result", {})
    reviews = result.get("reviews", [])

    if not reviews:
        return jsonify({"error": "No reviews found."}), 404

    top_reviews, bottom_reviews = extract_top_and_bottom_reviews(reviews)
    key_phrases = {
        "top": extract_key_phrases_from_reviews(top_reviews),
        "bottom": extract_key_phrases_from_reviews(bottom_reviews)
    }

    return jsonify({
        "restaurant": result.get("name"),
        "rating": result.get("rating"),
        "top_reviews": top_reviews,
        "bottom_reviews": bottom_reviews,
        "key_phrases": key_phrases
    })