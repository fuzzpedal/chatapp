""" Login """

import hashlib
import json

import base
import constants


class Login(base.BaseHandler):
    
    def response(self):
        result = {"status": 200}
        
        users = self.db.chat_users
        
        username = self.args.get('username', '')
        password = self.args.get('password', '')
        
        user = users.find_one({'username': username})
        
        if user and user.get('password') == hashlib.sha224(password).hexdigest():
            result = {
                "status": 200,
                "message": "Logged in",
            }
            # no active conversations on first login
            user['active_conversations'] = []
            user['status'] = constants.STATUS_ONLINE
            users.save(user)
        else:
            result = {
                "status": 401,
                "message": "Bad username/password combination",
            }
                
        return self.args.get('callback')+'('+json.dumps(result)+')'
