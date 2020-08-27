from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth


# Initialize application object
app = Flask(__name__, static_url_path = "/")

# Initialize HTTPBasicAuth
auth = HTTPBasicAuth()

# login credentials
@auth.get_password
def get_password(email):
    if email == "muchumimaina94@gmail.com":
        return "welcome"
    else:
        return None

# Decorator function to send unauthorized access error message to external clients
# Return 403 instead of 401 to restrict browsers from displaying the default auth dialog   
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error' : 'Unauthorized access'}), 403)

# an error handler for a bad request from a user
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad Request'}), 400)

# an error handler for a resource not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)


# Memory data structure acting as data storage for my minimal flask restful api
lessons = [
    {
        'id' : 1,
        'topic' : 'Big O Notation',
        'description' : 'Algorithms Classification, Worst-case Scenario',
        'covered' : 'false'
    },
    {
        'id' : 2,
        'topic' : 'Data Structures',
        'description' : 'Dictionaries, Lists, Tuples, Arrays',
        'covered' : 'true'
    },
    {
        'id' : 3,
        'topic' : 'Object Oriented Programming',
        'description' : 'Classes, Objects, Functions, Methods',
        'covered' : 'true',
    },
    {
        'id' : 4,
        'topic' : 'Python Frameworks',
        'description' : 'Django, Flask, Bottle, Pyramid',
        'covered' : 'false'
    },
    {
        'id' : 5,
        'topic' : 'Python Applicable Fields',
        'description' : 'Technical Areas Where Python Is Applicable',
        'covered' : 'false'
    }
]


# A helper function that generates a public version of a lesson to send to the client
def make_public_lesson(lesson):
    new_lesson = {}
    for field in lesson:
        if field == 'id':
            new_lesson['uri'] = url_for('get_lesson', id = lesson['id'], _external = True)
        else:
            new_lesson[field] = lesson[field]
    return new_lesson   

# HTTP GET request to get all lessons
@app.route('/LessonPlanner/api/v1/lessons', methods = ['GET'])
@auth.login_required
def get_lessons():
    return jsonify({'lessons' : list(map(make_public_lesson, lessons))})

# HTTP GET request to get a single lesson
@app.route('/LessonPlanner/api/v1/lessons/<int:id>', methods = ['GET'])
@auth.login_required
def get_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    return jsonify({'lesson' : make_public_lesson(lesson[0])})

# HTTP POST request to create a new lesson
@app.route('/LessonPlanner/api/v1/lessons', methods = ['POST'])
@auth.login_required
def create_lesson():
    if not request.json or not 'topic' in request.json:
        abort(400)
    lesson = {
        'id' : lessons[-1]['id'] + 1,
        'topic' : request.json['topic'],
        'description' : request.json.get('description', ""),
        'covered' : 'false'  
    }
    lessons.append(lesson)
    return jsonify({'lesson' : make_public_lesson(lesson)}), 201

# HTTP PUT request to update a lesson
@app.route('/LessonPlanner/api/v1/lessons/<int:id>', methods = ['PUT'])
@auth.login_required
def update_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'topic' in request.json and type(request.json['topic']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'covered' in request.json and type (request.json['covered']) is not bool:
        abort(400)
    lesson[0]['topic'] = request.json.get('topic', lesson[0]['topic'])
    lesson[0]['description'] = request.json.get('description', lesson[0]['description'])
    lesson[0]['covered'] = request.json.get('covered', lesson[0]['covered'])
    return jsonify({'lesson' : make_public_lesson(lesson[0])})

# HTTP DELETE request to delete a lesson
@app.route('/LessonPlanner/api/v1/lessons/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_lesson(id):
    lesson = list(filter(lambda l: l['id'] == id, lessons))
    if len(lesson) == 0:
        abort(404)
    lessons.remove(lesson[0])
    return jsonify({'result' : True})


# Run server
if __name__ == '__main__':
    app.run(debug=True)
                   
    
    
    

