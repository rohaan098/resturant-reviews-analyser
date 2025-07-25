import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [result, setResult] = useState(null);

  const handleAutocomplete = async (e) => {
    const input = e.target.value;
    setQuery(input);
    if (input.length > 1) {
      const res = await axios.get(`/autocomplete?q=${input}`);
      setSuggestions(res.data.suggestions);
    }
  };

  const handleSelectSuggestion = async (name) => {
    setQuery(name);
    setSuggestions([]);
    const res = await axios.get(`/autocomplete?q=${name}`);
    const place_id = res.data.place_ids?.[0] || "";
    fetchReviewData(place_id);
  };

  const fetchReviewData = async (placeId) => {
    const res = await axios.get(`/reviews?place_id=${placeId}`);
    setResult(res.data);
  };

  return (
    <div className="container">
      <h1>🍽️ Restaurant Review Insights</h1>
      <input
        type="text"
        placeholder="Search a restaurant..."
        value={query}
        onChange={handleAutocomplete}
        className="search-box"
      />
      {suggestions.length > 0 && (
        <ul className="suggestions">
          {suggestions.map((s, i) => (
            <li key={i} onClick={() => handleSelectSuggestion(s)}>{s}</li>
          ))}
        </ul>
      )}
      {result && (
        <div className="results">
          <h2>{result.restaurant} ({result.rating} ⭐)</h2>
          <div className="phrases">
            <h3>👍 Key Positive Phrases</h3>
            <ul>{result.key_phrases.top.map((k, i) => <li key={i}>{k}</li>)}</ul>
            <h3>👎 Key Negative Phrases</h3>
            <ul>{result.key_phrases.bottom.map((k, i) => <li key={i}>{k}</li>)}</ul>
          </div>
          <div className="reviews">
            <h3>Top Reviews</h3>
            {result.top_reviews.map((r, i) => (
              <blockquote key={i}>{r.text} — <i>{r.author_name}</i></blockquote>
            ))}
            <h3>Worst Reviews</h3>
            {result.bottom_reviews.map((r, i) => (
              <blockquote key={i}>{r.text} — <i>{r.author_name}</i></blockquote>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;