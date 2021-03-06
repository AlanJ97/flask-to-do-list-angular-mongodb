from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

# INITIALIZE APP
app = Flask(__name__)

# DATABASE
app.config['MONGO_DBNAME'] = 'meantask'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/meantask'

mongo = PyMongo(app)
CORS(app)

# ROUTES
@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    tasks = mongo.db.tasks
    result = []
    for field in tasks.find():
        result.append({'_id': str(field['_id']), 'title': field['title']})
    return jsonify(result)

@app.route('/api/task', methods=['POST'])
def add_task():
    tasks = mongo.db.tasks
    title = request.get_json()['title']
    task_id = tasks.insert({'title' : title})
    new_task = tasks.find_one({'_id' : task_id})

    result = {'title' : new_task['title']}
    return jsonify({'result' : result})


@app.route('/api/task/<id>', methods = ['PUT'])
def update_task(id):
    tasks = mongo.db.tasks
    title = request.get_json()['title']
    tasks.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'title': title}}, upsert=False)
    new_task = tasks.find_one({'_id': ObjectId(id)})
    result = {'title' : new_task['title']}

    return jsonify({'result' : result})

@app.route('/api/task/<id>', methods = ['DELETE'])
def delete_task(id):
    tasks = mongo.db.tasks
    response = tasks.delete_one({'_id' : ObjectId(id)})
    if response.deleted_count == 1:
        result = {'message' : 'record has been deleted'}
    else:
        result = {'message' : 'record no found, no deleted'}
    return jsonify({'result': result})

# RUN APP   
if __name__ == '__main__':
    app.run(debug = True)