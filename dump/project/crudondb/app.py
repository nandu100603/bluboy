from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import os
import threading
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:system@localhost/nandu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    tokenid = db.Column(db.String(20), unique=True, nullable=False)

with app.app_context():
    db.create_all()

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def push_users_from_file():
    #time.sleep(1)  # Ensure the server has time to start
    file_path = os.path.join(os.path.dirname(__file__), 'push.json')
    json_data = read_json_data(file_path)
    with app.app_context():
        for user_data in json_data['users']:
            user = User.query.filter_by(userid=user_data['userid']).first()
            if user:
                user.tokenid = user_data['tokenid']
            else:
                user = User(userid=user_data['userid'], tokenid=user_data['tokenid'])
                db.session.add(user)
        db.session.commit()
    #print('Data has been inserted/updated successfully.')

@app.route('/fetch', methods=['GET'])
def fetch_users():
    users = User.query.all()
    users_list = [{'userid': user.userid, 'tokenid': user.tokenid} for user in users]
    return jsonify(users_list)

@app.route('/push', methods=['POST'])
def push_users():
    json_data = request.get_json()
    for user_data in json_data['users']:
        user = User.query.filter_by(userid=user_data['userid']).first()
        if user:
            user.tokenid = user_data['tokenid']
        else:
            user = User(userid=user_data['userid'], tokenid=user_data['tokenid'])
            db.session.add(user)
    db.session.commit()
    return 'Data has been inserted/updated successfully.'

@app.route('/delete', methods=['POST'])
def delete_users():
    json_data = request.get_json()
    for user_data in json_data['users']:
        user = User.query.filter_by(userid=user_data['userid']).first()
        if user:
            db.session.delete(user)
    db.session.commit()
    return 'Data has been deleted successfully.'

if __name__ == '__main__':
    # Start the data pushing in a separate thread
    threading.Thread(target=push_users_from_file).start()
    # Run the Flask server
    app.run(debug=True)
