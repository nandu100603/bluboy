from flask import Flask, render_template, redirect, url_for, jsonify,request
import json
import os

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/selecteduser', methods=["GET"])
def users():
    with open('usernames.json', 'r') as f:
        gusers=json.load(f)
        final= jsonify(gusers)
    return final
@app.route('/user')
def user():
    with open('users.json', 'r') as b:
        gusers=json.load(b)
    return jsonify(gusers)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Process the data (e.g., save to a database)
    print("Received data:", data)
    with open('final.json', 'w') as f:
        json.dump(data, f, indent=2)
    

    return jsonify({"message": "Data received successfully", "data": data}), 200

@app.route('/final', methods=['GET'])
def view_data():
    if not os.path.exists('final.json'):
        return jsonify({"error": "No data found"}), 404

    with open('final.json', 'r') as f:
        data = json.load(f)

    return jsonify(data), 200

if __name__==('__main__'):
    app.run(debug=True)
