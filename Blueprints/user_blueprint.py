from flask import Blueprint, render_template, session,abort, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime
import os
from database.DBQuery import DBQuery
from tokens.__init__ import get_token,token_required


app_user = Blueprint('app_user',__name__)


@app_user.route('/login', methods=['POST'])
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

@app_user.route('/signin',methods=['POST'])
def sign_in():

    db_query = DBQuery()

    try:
        email = request.get_json()['email']
        password = request.get_json()['password']
        name = request.get_json()['name']
        height = request.get_json()['height']

        obj = {'email':email,'password':password,'name':name,'height':height}

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


@app_user.route('/info',methods=['GET'])
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
