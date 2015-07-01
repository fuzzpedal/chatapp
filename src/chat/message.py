""" Message """

from time import time
import json

import base


class Message(base.BaseHandler):
    
    def response(self):
        result = {"status": 200}
        
        user = self.authenticate()
        if not user:
            result = {
                "status": 401,
                "message": "Unauthorised",
            }
        else:
            messages = self.db.chat_messages
            
            message = {
                "from": user.get('username'),
                "to": self.args.get('to'),
                "message": self.args.get('message'),
                "timestamp": time(),
           }
            messages.insert(message)
        
        
        return self.args.get('callback')+'('+json.dumps(result)+')'
