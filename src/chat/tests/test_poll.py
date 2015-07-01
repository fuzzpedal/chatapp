import json
import sha
from time import time
import unittest
import urllib
import urllib2

import pymongo

import base


class TestPoll(base.BaseTest):
    
    def setUp(self):
        super(TestPoll, self).setUp()
        self.url = "http://localhost:8080/poll"
                
        testuser1 = {'username': 'testuser1',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     'contacts': ['testuser2',],
                     "active_conversations": ['#testroom',],
                     }
        testuser2 = {'username': 'testuser2',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     'contacts': ['testuser1',],
                     "active_conversations": ['#testroom',],
                     }
        testuser3 = {'username': 'testuser3',
                     'password': sha.new('password').hexdigest(),
                     'status': 'online',
                     'contacts': []
                     }
        self.users.insert(testuser1)
        self.users.insert(testuser2)
        self.users.insert(testuser3)
        
        self.message1_time = time()
        testmessage1 = {'from': 'testuser1',
                        'to': '#testroom',
                        'timestamp': self.message1_time,
                        'message': 'This is a test',
                        }
        self.message2_time = time()
        testmessage2 = {'from': 'testuser2',
                        'to': '#testroom',
                        'timestamp': self.message2_time,
                        'message': 'This is a reply',
                        }
        self.messages.insert(testmessage1)
        self.messages.insert(testmessage2)
        
        conversation = {'id': '#testroom',
                        'contacts': ['testuser1', 'testuser2'],
                    }
    
        self.conversations.insert(conversation)
        
    
    def tearDown(self):
        self.users.remove({'username': 'testuser1'})
        self.users.remove({'username': 'testuser2'})
        self.users.remove({'username': 'testuser3'})
        self.messages.remove({'from': 'testuser1'})
        self.messages.remove({'from': 'testuser2'})
        self.conversations.remove({'id': '#testroom'});
        

    def test_message_ok(self):
        params = {'username': 'testuser1',
                  'password': 'password',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['conversations'][0]['messages'][0].get('message'), 'This is a test')
        self.assertEqual(data['conversations'][0]['messages'][1].get('message'), 'This is a reply')
    
    
    def test_contacts_ok(self):
        params = {'username': 'testuser2',
                  'password': 'password',
                  'callback': 'testchat',
                  }
                
        data = self.getData(params)
        
        assert(data['conversations'][0]['contacts'][0].get('username') == 'testuser1')
        assert(data['conversations'][0]['contacts'][1].get('username') == 'testuser2')
        
