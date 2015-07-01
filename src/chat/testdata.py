""" Register """

import hashlib
import pymongo

import constants


def add_test_data():
    
    connection = pymongo.MongoClient()
    db = connection.chat_db
    users = db.chat_users
    conversations = db.chat_conversations
    
    users.remove({'username': 'dexter'})
    users.remove({'username': 'deedee'})
    users.remove({'username': 'johnnybravo'})
    conversations.remove({'id': '#someroom'})
    
    password_hash = hashlib.sha224("password").hexdigest()
    user = {
        "username": "dexter",
        "password": password_hash,
        "contacts": ['deedee', 'johnnybravo'],
        "status": constants.STATUS_ONLINE,
        "active_conversations": ['#someroom',],
    }
    
    users.insert(user)
    
    user = {
        "username": 'deedee',
        "password": password_hash,
        "contacts": ['dexter',],
        "status": constants.STATUS_ONLINE,
        "active_conversations": ['#someroom',],
    }
    
    users.insert(user)
    
    user = {
        "username": 'johnnybravo',
        "password": password_hash,
        "contacts": ['dexter',],
        "status": constants.STATUS_AWAY,
        "active_conversations": ['#someroom',],
    }
    
    users.insert(user)
    
    conversation = {
        "id": "#someroom",
        "contacts": ["dexter", "deedee"]
    }
    
    conversations.insert(conversation)