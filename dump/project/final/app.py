from flask import Flask, render_template, redirect, url_for, jsonify,request
from flask_sqlalchemy import SQLAlchemy
import json
import os
 
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:system@localhost/nandu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class templates(db.Model):
    __tablename__='template'
    title=db.Column(db.String(20),primary_key=True)
    message=db.Column(db.String(100),unique=True,nullable=False)
 
with app.app_context():
    db.create_all()
def read_json_data(file_path):
    with open(file_path,'r') as file:
        return json.load(file)
@app.route('/templatesfetchfromdb',methods=['GET'])
def temp_fetch():
    template=templates.query.all()
    temp_list=[{'title':i.title,'message':i.message}for i in template]
    return jsonify(temp_list)
@app.route('/pushtemplatetodb', methods=['POST'])
def push_templates():
    json_data = request.get_json()
    for temp_data in json_data['template']:
        temp = templates.query.filter_by(title=temp_data['title']).first()
        if temp:
            temp.message = temp_data['message']
        else:
            temp = templates(title=temp_data['title'], message=temp_data['message'])
            db.session.add(temp)
    db.session.commit()
    return 'Data has been inserted/updated successfully.'
 
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