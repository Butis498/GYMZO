from database.DBManager import DBManager


class DBQuery():

    def __init__(self):

        self.db_manager = DBManager()
        self.db_manager.set_connection()
        self.db = self.db_manager.connection['GYMZO']

    
    def add_document(self,collection:str,json:dict):
        
        collection_db = self.db[collection]
        collection_db.insert_one(json)

    def find_document(self,collection:str,json:dict):
        collection_db = self.db[collection]

        user = collection_db.find_one(json)

        return user

    def find_documents(self,collection:str,json:dict):
        collection_db = self.db[collection]

        user = collection_db.find(json)

        return user

    def clear_db(self):
        pass
 







