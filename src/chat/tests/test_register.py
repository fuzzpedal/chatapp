import json
import unittest
import urllib
import urllib2

import pymongo

import base


class TestRegister(base.BaseTest):
    
    def setUp(self):
        super(TestRegister, self).setUp()
        self.url = "http://localhost:8080/register"
        
        testuser2 = {'username': 'testuser_exists',
                     'password': 'password',
                     }
        self.users.insert(testuser2)
    
    def tearDown(self):
        self.users.remove({'username': 'testuser_exists'})
        

    def test_ok(self):
        params = {'username': 'testuser1',
                  'password': 'password',
                  'password2': 'password',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 201)
    
    def test_duplicate_fail(self):
        params = {'username': 'testuser_exists',
                  'password': 'password',
                  'password2': 'password',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 409)
    
    def test_password_invalid_fail(self):
        params = {'username': 'testuser2',
                  'password': 'pass',
                  'password2': 'pass',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 400)
    
    def test_password_mismatch_fail(self):
        params = {'username': 'testuser2',
                  'password': 'password',
                  'password2': 'password2',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 400)
        
