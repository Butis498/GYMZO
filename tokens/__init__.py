from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os

def get_token(user): 
 

    if user == None:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    token = jwt.encode({'id': str(user['_id']), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, os.getenv('SECRET_KEY'))  
    return jsonify({'token' : token,'id':str(user['_id'])}) 


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})


        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'),algorithms="HS256")
        except:
            return jsonify({'message': 'token is invalid'}),401

        return f(data, *args, **kwargs)

   return decorator