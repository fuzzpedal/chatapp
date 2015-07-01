import json
import unittest
import urllib
import urllib2

import pymongo


class BaseTest(unittest.TestCase):
    def setUp(self):
        connection = pymongo.MongoClient()
        db = connection.chat_db
        self.users = db.chat_users
        self.messages = db.chat_messages
        self.conversations = db.chat_conversations
    
    def getData(self, params):
        request = urllib2.Request("%s?%s" % (self.url, urllib.urlencode(params)))
        response = urllib2.urlopen(request)
        return json.loads(response.read()[9:-1])
