from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client.todo_db
todos_collection = db.todos

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = []
    for todo in todos_collection.find():
        todos.append({
            'id': str(todo['_id']),
            'task': todo['task']
        })
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = {'task': data['task']}
    result = todos_collection.insert_one(new_todo)
    return jsonify({'id': str(result.inserted_id)})

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    result = todos_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
