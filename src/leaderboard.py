"""This module contains utilities for accessing and modifying the game leaderboard"""

import os

import pymongo
import pymongo.errors
import dotenv

from utils import difficulties, MAX_LEADERS

dotenv.load_dotenv()


class Leaderboard:
    """A class that connects to the database and can make changes"""

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
        """Get the top MAX_LEADERS scores for a given difficulty"""
        return list(self.database[difficulty].find().sort('time').limit(MAX_LEADERS))

    def is_high_score(self, difficulty, time):
        """Checks if a given time is a high score for the difficulty"""
        tops = self.get_top(difficulty)
        if len(tops) < MAX_LEADERS:
            return True
        return time < tops[MAX_LEADERS-1]['time']

    def add_score(self, difficulty, time, name):
        """Add a score to the database"""
        self.database[difficulty].insert_one({'time': time, 'name': name})

    def clear_database(self):
        """Clears the database"""
        for diff in difficulties:
            self.database[diff].delete_many({})
