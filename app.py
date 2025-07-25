from flask import Flask, render_template, request
from utils import get_google_reviews, extract_key_phrases

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        restaurant_name = request.form['restaurant_name']
        reviews = get_google_reviews(restaurant_name)
        key_phrases = extract_key_phrases(reviews)
        return render_template('index.html', key_phrases=key_phrases, restaurant=restaurant_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)