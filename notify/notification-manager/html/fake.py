from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Save the data to a JSON file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    return jsonify({"message": "Data received successfully", "data": data}), 200

@app.route('/api/view-data', methods=['GET'])
def view_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data found"}), 404

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
