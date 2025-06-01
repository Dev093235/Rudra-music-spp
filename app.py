# app.py
from flask import Flask, jsonify, request
import requests
import os

# Flask application ko initialize karein
app = Flask(__name__)

# Deezer API ka base URL
# Hum yahan se music data fetch karenge
DEEZER_API_BASE_URL = "https://api.deezer.com"

# Home route - jab koi root URL par visit karega
@app.route('/')
def home():
    return "Welcome to the Music API Wrapper! Use /search/tracks?q=<query> to search for tracks."

# Search tracks ke liye API endpoint
# Example URL: /search/tracks?q=hello
@app.route('/search/tracks')
def search_tracks():
    # URL se 'q' parameter lein (search query)
    query = request.args.get('q')

    # Agar 'q' parameter nahi mila, toh error return karein
    if not query:
        return jsonify({"error": "Please provide a 'q' parameter for your search query."}), 400

    # Deezer API ko bhejne ke liye parameters set karein
    params = {"q": query}

    try:
        # Deezer API se data fetch karein
        response = requests.get(f"{DEEZER_API_BASE_URL}/search/track", params=params)
        response.raise_for_status()  # HTTP errors (4xx ya 5xx) ke liye exception uthayein

        # Response ko JSON mein parse karein
        data = response.json()

        # Parsed data ko JSON format mein return karein
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # Agar Deezer API se data fetch karte waqt koi error aaye
        return jsonify({"error": f"Failed to fetch data from Deezer API: {e}"}), 500

# Jab script seedhe run ho, toh is block ka code chalega
if __name__ == '__main__':
    # Render deployment ke liye 'PORT' environment variable ka use karein
    # Agar PORT set nahi hai, toh default 5000 use karein
    port = int(os.environ.get('PORT', 5000))
    # Application ko sabhi network interfaces (0.0.0.0) par run karein
    # Taki Render use access kar sake
    app.run(host='0.0.0.0', port=port)
