import json
import sha
from time import time
import unittest
import urllib
import urllib2

import pymongo

import base


class TestMessage(base.BaseTest):
    
    def setUp(self):
        super(TestMessage, self).setUp()
        self.url = "http://localhost:8080/message"
        
        testuser1 = {'username': 'testuser1',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     'contacts': ['testuser2',]
                     }
        testuser2 = {'username': 'testuser2',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     'contacts': ['testuser1',]
                     }
        self.users.insert(testuser1)
        self.users.insert(testuser2)
        
    
    def tearDown(self):
        self.users.remove({'username': 'testuser1'})
        self.users.remove({'username': 'testuser2'})
        self.messages.remove({'from': 'testuser2'})
        

    def test_message_ok(self):
        params = {'username': 'testuser2',
                  'password': 'password',
                  'to': 'testuser1',
                  'message': 'This is a test.',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        message = self.messages.find_one({"from": "testuser2"})
        
        self.assertEqual(message.get('message'), 'This is a test.')
    
    def test_auth_fail(self):
        params = {'username': 'testuser_noexist',
                  'password': 'password',
                  'to': 'testuser1',
                  'message': 'This is a test.',
                  'callback': 'testchat',
                  }
                  
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 401)
        
