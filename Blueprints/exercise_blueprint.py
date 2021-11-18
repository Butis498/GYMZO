from flask import Blueprint, render_template, session,abort, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime
import os
from database.DBQuery import DBQuery
from tokens.__init__ import get_token,token_required

app_exercise = Blueprint('app_exercise',__name__)

@app_exercise.route('/get_excercise',methods=['GET'])
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


@app_exercise.route('/get_exercises',methods=['POST'])
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

@app_exercise.route('/register_exercise',methods=['POST'])
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


@app_exercise.route('/register-record',methods=['POST'])
@token_required
def register_record(user):
    db_query = DBQuery()

    try:
        exercise_id = request.get_json()['exercise_id']
        weight = request.get_json()['weight']
        reps = request.get_json()['reps']
        sets = request.get_json()['sets']
        exercise = db_query.find_document('exercises',{"_id":ObjectId(exercise_id)})

        obj = {'exercise_id':exercise_id,'weight':weight,'reps':reps,'sets':sets,'routine_id':str(exercise['routine_id']),'user_id':user['id']}

        db_query.add_document('user_records',obj)

        succesful_msg = {
            'Error':'None'
        }

        return jsonify(succesful_msg), 200


    except KeyError as err:

        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400

@app_exercise.route('/get_rocords',methods=['POST'])
@token_required
def get_records(user):

    db_query = DBQuery()
    try:
        exercise_id = request.get_json()['exercise_id']
        exercises = db_query.find_documents('user_records',{"exercise_id":exercise_id})
        objs = []
        for exercise in exercises:
            obj = {
                'date':ObjectId(exercise['_id']).generation_time.strftime('%m/%d/%Y'),
                '_id':exercise['_id'],
                'weight':exercise['weight'],
                'sets':exercise['sets'],
                'routine_id':exercise['routine_id'],
                'user_id':exercise['user_id']
            }
            objs.append(obj)
            

        return dumps(objs),200


    except KeyError as err:

        error_request = {
            'Error':str(err)
        }
        return jsonify(error_request), 400
