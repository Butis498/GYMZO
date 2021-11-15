from flask import Blueprint, render_template, session,abort, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime
import os
from database.DBQuery import DBQuery
from tokens.__init__ import get_token,token_required

app_routine = Blueprint('app_routine',__name__)


@app_routine.route('/get_routine',methods=['GET'])
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

@app_routine.route('/get_routines',methods=['POST'])
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

@app_routine.route('/register_routine',methods=['POST'])
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


