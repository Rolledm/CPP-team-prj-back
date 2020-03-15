from flask import Flask
from flask import request
import json
import entities
from pymongo import MongoClient

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
client = MongoClient()
db = client['user']

@app.route('/user', methods=['GET'])
def userAPI():
    user_res = db['users'].find_one({"login": request.args.get('login')}) 

    try:
        user = entities.User(user_res['id'], user_res['login'], user_res['password'], user_res['eMail'], user_res['Name'])
        if user.password == request.args.get('password'):
            return json.dumps(user.__dict__)
    except:
        pass

@app.route('/user', methods=['POST'])
def userAdd():
    try:
        max_id = db['users'].find_one(sort=[("id", -1)])['id']
    except:
        max_id = -1
    data = request.get_json()

    login = data['login']
    password = data['password']
    eMail = data['eMail']
    Name = data['Name']

    user = entities.User(max_id + 1, login, password, eMail)

    db['users'].insert_one(user.__dict__)

    return '{"result": "OK"}'


@app.route('/debug')
def debug():
    return "Test"

print("Starting server...")

if __name__ == '__main__':
    app.run()
