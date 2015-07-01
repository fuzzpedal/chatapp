""" Register """

import json
import hashlib

import base
import constants


class Register(base.BaseHandler):
    
    def response(self):
        result = {"status": 200}
        users = self.db.chat_users
        
        username = self.args.get('username', '')
        password = self.args.get('password', '')
        password2 = self.args.get('password2', '')
        
        if len(username.strip()) < constants.MIN_USERNAME_LENGTH:
            result = {"status": 400,
                      "message": "Username must be over %s characters long" % constants.MIN_USERNAME_LENGTH,
                      }
        
        elif users.find_one({'username': username}):
            result = {"status": 409,
                      "message": "This username has already been taken",
                      }
        
        elif len(password) < constants.MIN_PASSWORD_LENGTH:
            result = {"status": 400,
                      "message": "Password must be over %s characters long" % constants.MIN_PASSWORD_LENGTH,
                      }
            
        elif password != password2:
            result = {"status": 400,
                      "message": "Passwords do not match",
                      }
        
        else:
            password_hash = hashlib.sha224(password).hexdigest()
            user = {"username": username,
                    "password": password_hash,
                    "status": constants.STATUS_ONLINE,
                    }
            users.insert(user)
            result = {"status": 201,
                      "message": "User created",
                      }
                
        return self.args.get('callback')+'('+json.dumps(result)+')'
