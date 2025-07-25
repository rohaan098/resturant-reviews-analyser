import os
from flask import Flask, render_template, request
from utils import get_google_reviews, extract_key_phrases

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    restaurant_name = request.form['restaurant_name']
    api_key = os.environ.get('GOOGLE_API_KEY')
    reviews = get_google_reviews(restaurant_name, api_key)
    key_phrases = extract_key_phrases(reviews)
    return render_template('index.html', key_phrases=key_phrases, restaurant=restaurant_name)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '')
    api_key = os.environ.get('GOOGLE_API_KEY')
    suggestions = get_autocomplete_suggestions(query, api_key)
    return jsonify(suggestions)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port)
