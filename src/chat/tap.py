from twisted.application import internet

from twisted.internet import defer
from twisted.web import server, resource
from twisted.python import usage

from join import Join
from login import Login
from message import Message
from poll import Poll
from register import Register

import testdata


HTML = \
"""
<html>
    <head><title>Chat Service</title></head>
    <body><h1>Chat Service</h1></body>
</html>"""
 
class ChatResource(resource.Resource):
    isLeaf = True
        
    def render_GET(self, request):
        def _(res):
            request.write(res)
            request.finish()
		
        d =  defer.maybeDeferred(self.handle_request, request)
        d.addCallback(_)
        return server.NOT_DONE_YET
    
    def handle_request(self, request):
        args = {}
        for k, v in request.args.items():
            args.update({k: v[0]},)
        
        if len(request.postpath[0]) and not args.get('callback'):
            request.setResponseCode(400)
            return HTML
        
        if 'register' in request.postpath:
            register = Register(request, args)
            return register.response()
        
        if 'login' in request.postpath:
            login = Login(request, args)
            return login.response()
        
        if 'poll' in request.postpath:
            poll = Poll(request, args)
            return poll.response()
        
        if 'message' in request.postpath:
            message = Message(request, args)
            return message.response()
        
        if 'join' in request.postpath:
            join = Join(request, args)
            return join.response()
        
        else:
            return """
<html>
    <head><title>Chat Service</title></head>
    <body><h1>Chat Service</h1></body>
</html>"""
			
	
        	
 
 
class Options(usage.Options):
    pass
 
 
def makeService(config):
    testdata.add_test_data()
    site = server.Site(ChatResource())
    return internet.TCPServer(8080, site)
