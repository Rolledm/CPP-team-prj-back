from flask import Flask
from flask import request
import json
import entities
from pymongo import MongoClient
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        user = entities.User(user_res['id'], user_res['login'], user_res['password'], user_res['eMail'], user_res['name'])
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
    name = data['name']

    user = entities.User(max_id + 1, login, password, eMail, name)

    db['users'].insert_one(user.__dict__)

    return '{"result": "OK"}'


@app.route('/debug')
def debug():
    return '{"Test": "test"}'

@app.route('/run', methods=["POST"])
def run():
    file = request.files['file']
    file.save("./temp_example/main.cpp")
    #data = request.get_json() TODO

    task_id = 0
    #user = db['users'].find_one({'login': data['login']})
    user = db['users'].find_one({'login': 'rld'})

    required_output = db['tasks'].find_one({'id': task_id})['answer']

    cmd = ["g++", "-o", "./temp_example/main", "./temp_example/main.cpp"]
    proc = subprocess.Popen(cmd)
    proc.wait()
    output = subprocess.check_output(["./temp_example/main"]).decode("utf-8")
    if output == required_output:
        user['taskId'] = str(int(user['taskId']) + 1)
        db['users'].save(user)
        return '{"result": "OK"}'
    else:
        return '{"result": "NOT OK}'
    
@app.route('/progress')
def progress():
    user_res = db['users'].find_one({"login": request.args.get('login')})
    try:
        retVal = user_res['taskId']
        return retVal
    except:
        pass

print("Starting server...")

if __name__ == '__main__':
    app.run()
