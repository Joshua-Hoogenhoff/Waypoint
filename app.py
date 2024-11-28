
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import datetime

app = Flask(__name__)
CORS(app)

# Database connection
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/community_map?retryWrites=true&w=majority")
db = client['community_map']
locations_collection = db['locations']

@app.route('/add-location', methods=['POST'])
def add_location():
    data = request.json
    user_id = data.get('userId')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    bio = data.get('bio', '')

    if not user_id or not city or not country:
        return jsonify({"error": "Invalid input"}), 400

    location_data = {
        "userId": user_id,
        "city": city,
        "state": state,
        "country": country,
        "bio": bio,
        "timestamp": datetime.datetime.utcnow()
    }

    locations_collection.update_one({"userId": user_id}, {"$set": location_data}, upsert=True)
    return jsonify({"message": "Location updated successfully"}), 200

@app.route('/get-locations', methods=['GET'])
def get_locations():
    locations = list(locations_collection.find({}, {"_id": 0}))
    return jsonify(locations), 200

@app.route('/delete-location', methods=['POST'])
def delete_location():
    data = request.json
    user_id = data.get('userId')

    if not user_id:
        return jsonify({"error": "Invalid input"}), 400

    locations_collection.delete_one({"userId": user_id})
    return jsonify({"message": "Location deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
