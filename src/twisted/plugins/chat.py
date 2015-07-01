from twisted.application.service import ServiceMaker
 
Chat = ServiceMaker(
    "Chat",
    "chat.tap",
    "Basic Chat Service",
    "chat"
)
