from pymongo import MongoClient

from Lost_Found_app.utils import *
from Lost_Found_app.Lost_Found_app.settings import *

# mongo_database, mongo_client = get_db_handle(DATABASE_NAME, DATABASE_HOST, DATABASE_PORT, USERNAME, PASSWORD)
# collections = get_collection_handle(mongo_database, COLLECTIONS_NAME)

# local
mongo_client = MongoClient('localhost', 27017)
mongo_database = mongo_client['lost_found_app']

users_collection = mongo_database['users']
registration_collection = mongo_database['registration_data']
comment_collection = mongo_database['comment']
announcements_collection = mongo_database['announcements']
chat_collection = mongo_database['chat']
messages_collection = mongo_database['messages']

# database methods
# db.get_collection
# collection.insert_many
# collection.find()
# collection.find_one()
# collection.find().count
# collection.aggregate()
# collection.update()
