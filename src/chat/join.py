""" Join """

import json

import base


class Join(base.BaseHandler):
    """ Creates conversation if none exists
        Adds conversation id to active_conversation on user
    """
    def response(self):
        result = {"status": 200}
        
        user = self.authenticate()
        if not user:
            result = {
                "status": 401,
                "message": "Unauthorised",
            }
        else:
            conversation_id = self.args.get('conversation_id')
            
            if not conversation_id.startswith('#') or len(conversation_id) < 2:
                result = {
                    "status": 400,
                    "message": "Bad request",
                }
            
            conversations = self.db.chat_conversations
            conversation = conversations.find_one({'id': conversation_id})
            if not conversation:
                conversation = {'id': conversation_id,
                                'contacts': [user.get('username'),]}
                conversations.insert(conversation)
            else:
                contacts = conversation.get('contacts')
                if user.get('username') not in contacts:
                    contacts.append(user.get('username'))
                conversation['contacts'] = contacts
                conversations.save(conversation)
                
            active_conversations = user.get('active_conversations', [])
            active_conversations.append(conversation_id)
            users = self.db.chat_users
            users.update(
                {'username': user.get('username')},
                {'$set': { 'active_conversations': active_conversations, },}
            )        
        
        return self.args.get('callback')+'('+json.dumps(result)+')'
