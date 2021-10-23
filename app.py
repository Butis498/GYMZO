from flask import Flask, jsonify, request
from error import Error
from database.DBQuery import DBQuery
import os
from tokens.__init__ import get_token,token_required
from bson.objectid import ObjectId
from bson.json_util import dumps, loads


app = Flask(__name__)



@app.route('/login', methods=['POST'])
def log_in():

    db_query = DBQuery()
    try:
        email = request.get_json()['email']
        password = request.get_json()['password']

        obj = {'email':email, 'password':password}
        user = db_query.find_document('users',obj)
        if user == None :

            error_request = {
            'Error':'Incorrect email or password'
            }
            return jsonify(error_request),401


        return get_token(user), 200
        

    except KeyError as err:

        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400

@app.route('/info',methods=['GET'])
@token_required
def get_info(user):
    db_query = DBQuery()
    try:
        user_data = db_query.find_document('users',{'_id':ObjectId(user['id'])})
        user_data['_id'] = user['id']
        return jsonify(user_data),200

    except:
        error_request = {
            'Error': 'Internal error'
        }
        return jsonify(error_request), 400 

@app.route('/get_excercise',methods=['GET'])
@token_required
def get_excercise(user):
    db_query = DBQuery()
    data = request.get_json()
    try:
        try:
            _id = data['id']

        except KeyError as err:
            error_request = {'Error':str(err)}
            return jsonify(error_request), 400

        exercise_data = db_query.find_document('excercises',{'_id':ObjectId(_id)})
        exercise_data['_id'] = _id
        return jsonify(exercise_data),200

    except:
        error_request = {
            'Error': 'Internal error'
        }
        return jsonify(error_request), 400

@app.route('/get_routine',methods=['GET'])
@token_required
def get_routine(user):
    db_query = DBQuery()
    data = request.get_json()
    try:

        try:
            _id = data['id']

        except KeyError as err:
            error_request = {'Error':str(err)}
            return jsonify(error_request), 400

        routine_data = db_query.find_document('routines',{'_id':ObjectId(_id)})
        routine_data['_id'] = _id
        return jsonify(routine_data),200

    except:
        error_request = {
            'Error': 'Internal error'
        }
        return jsonify(error_request), 400


@app.route('/get_routines',methods=['GET'])
@token_required
def get_routines(user):
    db_query = DBQuery()
    try:

        try:
            _id = user['id']

        except KeyError as err:
            error_request = {'Error':str(err)}
            return jsonify(error_request), 400

        routines_data = db_query.find_documents('routines',{'user_id':_id})
        return dumps(routines_data),200

    except:
        error_request = {
            'Error': 'Internal error'
        }
        return jsonify(error_request), 400

@app.route('/get_exercises',methods=['GET'])
@token_required
def get_exercises(user):
    db_query = DBQuery()
    data = request.get_json()
    try:

        try:
            routine_id = data['routine_id']

        except KeyError as err:
            error_request = {'Error':str(err)}
            return jsonify(error_request), 400

        routines_data = db_query.find_documents('exercises',{'user_id':user['id'],'routine_id':routine_id})
        return dumps(routines_data),200

    except:
        error_request = {
            'Error': 'Internal error'
        }
        return jsonify(error_request), 400


@app.route('/register_exercise',methods=['POST'])
@token_required
def register_excercise(user):
    db_query = DBQuery()
    data = request.get_json()

    try:
        name = data['name']
        sets = data['sets']
        reps = data['reps']
        has_weight = data['has_weight']
        user_id = user['id']
        routine_id = data['routine_id']

        data = {'name':name, 'sets':sets, 'reps':reps,'has_weight':has_weight, 'user_id':user_id,'routine_id':routine_id}
        db_query.add_document('exercises',data)
        exercise = db_query.find_document('exercises',data)
        message = {
            'message':'Succesfuly register exercise',
            'exercise_id': str(exercise['_id'])
        }

        return jsonify(message)

    except KeyError as err:
        
        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400



@app.route('/register_routine',methods=['POST'])
@token_required
def register_routine(user):
    db_query = DBQuery()
    data = request.get_json()

    try:
        name = data['name']
        order = data['order']
        user_id = user['id']

        data = {'name':name, 'order': order, 'user_id': user_id}
        db_query.add_document('routines',data)

        routine = db_query.find_document('routines',data)

        message = {
            'message':'Succesfuly register routine',
            'routine_id': str(routine['_id'])
        }

        return jsonify(message)

    except KeyError as err:

        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400


@app.route('/signin',methods=['POST'])
def sign_in():

    db_query = DBQuery()

    try:
        email = request.get_json()['email']
        password = request.get_json()['password']
        name = request.get_json()['name']
        height = request.get_json()['height']

        obj = {'email':email,'password':password,'name':name,'height':height}
        print(obj)

        db_query.add_document('users',obj)

        succesful_msg = {
            'Error':'None'
        }

        return jsonify(succesful_msg), 200


    except KeyError as err:

        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')
