#!.venv/bin/python

# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#HTTP Method	URI	Action
#GET	http://[hostname]/todo/api/v1.0/tasks	Retrieve list of tasks
#GET	http://[hostname]/todo/api/v1.0/tasks/[task_id]	Retrieve a task
#POST	http://[hostname]/todo/api/v1.0/tasks	Create a new task
#PUT	http://[hostname]/todo/api/v1.0/tasks/[task_id]	Update an existing task
#DELETE	http://[hostname]/todo/api/v1.0/tasks/[task_id]	Delete a task

from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)


tasks = [
   	{
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def public_task(task):
	new_task = dict()
	for k in task:
		if k == 'id':
			new_task[k] = url_for("get_task", id=task['id'], _external=True)
		else:
			new_task[k] = task[k]
	return new_task


@app.errorhandler(404)
def not_found(error):
	return make_response(
		jsonify(dict(error=error.name, code=error.code, description=error.description)),
		error.code
	)

# curl -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
	return jsonify(dict(tasks = [ public_task(t) for t in tasks ] ))

# curl -i http://localhost:5000/todo/api/v1.0/tasks/1
@app.route('/todo/api/v1.0/tasks/<int:id>', methods=['GET'])
def get_task(id):
	task = [ t for t in tasks if t.get('id', -1) == id ]
	if not task:
		abort(404)
	return jsonify(dict(task=task[0]))

# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)

	task = dict(
		id = tasks[-1].get('id', -1) + 1,
		title = request.json['title'],
		description = request.json.get('description', ""),
		done = False
	)
	tasks.append(task)
	return jsonify(dict(task=task)), 201

# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
	    abort(404)
	if not request.json:
	    abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
	    abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
	    abort(400)
	if 'done' in request.json and type(request.json['done']) is not bool:
	    abort(400)
	task[0]['title'] = request.json.get('title', task[0]['title'])
	task[0]['description'] = request.json.get('description', task[0]['description'])
	task[0]['done'] = request.json.get('done', task[0]['done'])
	return jsonify({'task': task[0]})

# curl -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
	task = [ t for t in tasks if t.get('id', -1) == id ]
	if not task:
		abort(404)
	tasks.remove(task[0])
	return jsonify(dict(result=True))


if __name__ == "__main__":
	app.run(debug=True)