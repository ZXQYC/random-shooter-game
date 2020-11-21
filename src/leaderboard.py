
import os

import pymongo
import pymongo.errors
import dotenv

from utils import difficulties

dotenv.load_dotenv()


class Leaderboard:
    """A class that connects to the database and can make changes"""
    TOP = 5

    def __init__(self, db_name='leaderboard'):
        """Creates a database handler"""
        key = os.getenv('ATLAS_KEY')
        self.valid = key is not None
        self.client = None
        self.database = None
        if self.valid:
            try:
                self.client = pymongo.MongoClient(key % db_name)
                self.database = self.client[db_name]
            except pymongo.errors.ConfigurationError:
                self.valid = False

    def get_top(self, difficulty):
        return list(self.database[difficulty].find().sort('time').limit(self.TOP))

    def is_high_score(self, difficulty, time):
        tops = self.get_top(difficulty)
        if len(tops) < self.TOP:
            return True
        return time < tops[self.TOP-1]['time']

    def add_score(self, difficulty, time, name):
        self.database[difficulty].insert_one({'time': time, 'name': name})

    def clear_database(self):
        for diff in difficulties:
            self.database[diff].delete_many({})
