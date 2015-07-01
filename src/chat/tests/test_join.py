import json
import sha
from time import time
import unittest
import urllib
import urllib2

import pymongo

import base


class TestJoin(base.BaseTest):
    
    def setUp(self):
        super(TestJoin, self).setUp()
        self.url = "http://localhost:8080/join"
        
        testuser1 = {'username': 'testuser1',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     }
        self.users.insert(testuser1)
        
        conversation = {'id': '#testroom',
                        'contacts': ['testuser1',],
                    }
    
        self.conversations.insert(conversation)
        
    
    def tearDown(self):
        self.users.remove({'username': 'testuser1'})
        self.conversations.remove({'id': '#testroom'});
        self.conversations.remove({'id': '#newroom'});
        

    def test_join_new_ok(self):
        params = {'username': 'testuser1',
                  'password': 'password',
                  'callback': 'testchat',
                  'conversation_id': '#newroom',
                  }
        
        conversation = self.conversations.find_one({'id': '#newroom'})
        self.assertEqual(conversation, None)
        
        data = self.getData(params)
        
        conversation = self.conversations.find_one({'id': '#newroom'})
        self.assertEqual(conversation.get('id'), '#newroom')
    
    def test_join_existing_ok(self):
        """ Check there is one conversation with the id #testroom
            and one after the query, also check the id is what we expect
        """
        params = {'username': 'testuser1',
                  'password': 'password',
                  'callback': 'testchat',
                  'conversation_id': '#testroom',
                  }
        
        num_conversations = len([item for item in self.conversations.find({'id': '#testroom'})])
        self.assertEqual(num_conversations, 1)
        
        data = self.getData(params)
        
        num_conversations = len([item for item in self.conversations.find({'id': '#testroom'})])
        self.assertEqual(num_conversations, 1)
        
        conversation = self.conversations.find_one({'id': '#testroom'})
        self.assertEqual(conversation.get('id'), '#testroom')
    
