from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your React app

# Sample data - replace with your actual data or database connection
CARDS = {
    "1": {
        "id": "1",
        "title": "Sunset at the Beach",
        "imageUrl": "https://via.placeholder.com/400x300",
        "description": "A beautiful sunset at the beach",
        "tags": ["sunset", "beach", "nature"]
    },
    "2": {
        "id": "2",
        "title": "Mountain Landscape",
        "imageUrl": "https://via.placeholder.com/400x300",
        "description": "Mountain landscape in the morning",
        "tags": ["mountain", "landscape", "nature"]
    },
    "3": {
        "id": "3",
        "title": "Urban Cityscape",
        "imageUrl": "https://via.placeholder.com/400x300",
        "description": "Urban cityscape at night",
        "tags": ["city", "urban", "night"]
    }
}

@app.route('/api/cards', methods=['GET'])
def get_all_cards():
    """Return all cards"""
    return jsonify(CARDS)

@app.route('/api/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    """Return a specific card by ID"""
    if card_id in CARDS:
        return jsonify(CARDS[card_id])
    return jsonify({"error": "Card not found"}), 404

if __name__ == '__main__':
    app.run(debug=True) 