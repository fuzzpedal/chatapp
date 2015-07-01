""" Poll """

from time import time
import json

import base


class Poll(base.BaseHandler):
    
    def response(self):
        result = {"status": 200}
                
        user = self.authenticate()
        if not user:
            result = {
                "status": 401,
                "message": "Unauthorised",
            }
            return self.args.get('callback')+'('+json.dumps(result)+')'
        
        # only get latest messages
        last_polled = user.get('last_polled') or 0
        
        result.update({"conversations": []})
        
        users = self.db.chat_users
        conversations = self.db.chat_conversations
        messages = self.db.chat_messages
        
        conversation_results = conversations.find({
            'id': {'$in': user.get('active_conversations', [])}
        })
        
        for conversation in conversation_results:
            result_conv = {
                'id': conversation.get('id'),
                'contacts': [],
                'messages': [],
            }
            
            contact_results = users.find({
                'username': {'$in': conversation.get('contacts', [])},
             }).sort("username")
            
            for contact in contact_results:
                result_conv['contacts'].append({
                    'username': contact.get('username'),
                    'status': contact.get('status'),
                })
            
            message_results = messages.find({
                "to": conversation.get('id'),
                "timestamp": {"$gt": last_polled},
            }).sort("timestamp")
             
            new_messages = []
            for message in message_results:
                result_conv['messages'].append({
                    'from': message.get('from'),
                    'to': message.get('to'),
                    'message': message.get('message'),
                    'timestamp': message.get('timestamp'),
                })
            
            result['conversations'].append(result_conv)
        
        user['last_polled'] = time()
        users.save(user)
        
        return self.args.get('callback')+'('+json.dumps(result)+')'
