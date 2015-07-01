import hashlib

import base


class TestLogin(base.BaseTest):
    
    def setUp(self):
        super(TestLogin, self).setUp()
        self.url = "http://chatserver:8080/login"
        
        testuser1 = {'username': 'testuser1',
                     'password': hashlib.sha224('password').hexdigest(),
                     }
        self.users.insert(testuser1)
    
    def tearDown(self):
        self.users.remove({'username': 'testuser1'})
        

    def test_ok(self):
        params = {'username': 'testuser1',
                  'password': 'password',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        self.assertEqual(data.get('status'), 200)
        
    
    def test_no_user_fail(self):
        params = {'username': 'testuser_noexist',
                  'password': 'password',
                  'callback': 'testchat',
                  }
        
        data = self.getData(params)
        
        self.assertEqual(data.get('status'), 401)
        
