from  database.DBConnection import DBConnection
from pymongo import  errors,MongoClient
from dotenv import load_dotenv
import os


class DBManager():

    def __init__(self):
        self.connection:MongoClient
        load_dotenv()
        self.URL = os.getenv('MONGO_URL')
        self.PORT = os.getenv('LOCAL_MONGO_PORT')


    def set_connection(self):

        self.connection = DBConnection().get_connection(url=self.URL,port=self.PORT)

        if self.connection == None:
            raise errors.ConnectionFailure('Could not set a connection')

    def close_connection(self):

        self.connection.close()
