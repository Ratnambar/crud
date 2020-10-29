from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api,Resource
from bson.objectid import ObjectId
import json
from bson.json_util import dumps
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)
api = Api(app)


app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)


class TodoList(Resource):
    def get(self):
        customers = mongo.db.mycol.find()
        return dumps(customers)

    def post(self):
        _json = request.get_json(force=True)
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']

        if _name and _email and _password and request.method == 'POST':
            _hashed_password = generate_password_hash(_password)

            id = mongo.db.mycol.insert({'name':_name,'email':_email,'pwd':_hashed_password})

            resp = jsonify("user added successfully.")
            resp.status_code = 200
            return resp
        else:
            not_found()

class TodoAgain(Resource):
    def get(self,id):
        customer = mongo.db.mycol.find_one({'_id':ObjectId(id)})
        resp = dumps(customer)
        return resp


    def put(self,id):
        _id = id
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']

        if _name and _email and _password and _id and request.method == 'PUT':
            _hashed_password = generate_password_hash(_password)

            mongo.db.mycol.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':{'name':_name,'email':_email,'pwd':_hashed_password}})
            resp = jsonify("User updated successfully.")
            return resp
        else:
            return not_found()

    def delete(self,id):
        mongo.db.mycol.delete_one({'_id':ObjectId(id)})
        resp = jsonify("User deleted successfully.")
        return resp




@app.errorhandler(404)
def not_found(error=None):
    message = {
    'status': 404,
    'message': 'Not found'+request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp



##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/')
api.add_resource(TodoAgain, '/todo/<id>')
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)