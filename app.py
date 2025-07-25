import os
from flask import Flask, render_template, request
from utils import get_google_reviews, extract_key_phrases

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    key_phrases = []
    reviews = []
    restaurant_name = ''
    if request.method == 'POST':
        restaurant_name = request.form['restaurant_name']
        reviews = get_google_reviews(restaurant_name, GOOGLE_API_KEY)
        key_phrases = extract_key_phrases(reviews)
    return render_template('index.html', key_phrases=key_phrases, restaurant=restaurant_name, reviews=reviews)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port)
