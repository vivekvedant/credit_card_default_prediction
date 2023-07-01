from pymongo import MongoClient
from src.constant.database import MONGO_DB_URL

class MongoDB:
    def __init__(self):
        self.mongodb_url = MONGO_DB_URL

    def get_database(self):
        client = MongoClient(self.mongodb_url)

        return client['Cluster0']
    
    def write_data(self,data,document_name):
        database = self.get_database()
        mydatabase = database[document_name]
        mydatabase.insert_one(data)
    


