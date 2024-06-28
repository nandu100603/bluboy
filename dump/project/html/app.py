from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:system@localhost/users'
db = SQLAlchemy(app)
class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    
def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['usernames']
def update_mysql_records(json_data):
    for user_data in json_data:
        user = Users(
            userid=user_data['userid'],
            username=user_data['username'],
            email=user_data['email']
        )
        db.session.add(user)
    db.session.commit()
@app.route('/update', methods=['GET'])
def update_users():
    json_data = read_json_data('data.json')
    update_mysql_records(json_data)
    return 'Data from JSON file has been added to the database.'
@app.route('/fetch', methods=['GET'])
def fetch_users():
    users = Users.query.all()
    users_list = [{
        'userid': user.userid,
        'username': user.username,
        'email': user.email
    } for user in users]
    return jsonify(users_list)

if __name__==('__main__'):
    app.run(debug=True)
