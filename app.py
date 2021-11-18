from flask import Flask, jsonify, request
from error import Error
from database.DBQuery import DBQuery
from tokens.__init__ import get_token,token_required
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime
from Blueprints.routine_bluprint import app_routine
from Blueprints.exercise_blueprint import app_exercise
from Blueprints.user_blueprint import app_user
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_exercise)
app.register_blueprint(app_user)
app.register_blueprint(app_routine)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
