from  database.DBConnection import DBConnection
from pymongo import  errors,MongoClient
from dotenv import load_dotenv
import os
from database.Singleton import Singleton

class DBManager(metaclass=Singleton):

    def __init__(self):
        self.connection:MongoClient
        load_dotenv()
        self.URL = os.getenv('MONGO_URL')
        self.PORT = os.getenv('LOCAL_MONGO_PORT')
        self.set_connection()


    def set_connection(self):

        self.connection = DBConnection().get_connection(url=self.URL,port=self.PORT)

        if self.connection == None:
            raise errors.ConnectionFailure('Could not set a connection')

    def close_connection(self):

        self.connection.close()
