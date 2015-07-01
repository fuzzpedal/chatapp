""" Base """

import pymongo


class BaseHandler(object):
    
    def __init__(self,request, args):
        self.request = request
        self.args = args
        connection = pymongo.MongoClient()
        self.db = connection.chat_db
        self.request.setHeader('Content-Type', 'application/javascript')
    
    def authenticate(self):
        username = self.args.get('username', '')
        password = self.args.get('password', '')
        users = self.db.chat_users
        user = users.find_one({'username': username})
        return user
    
    def response(self):
        pass
