from twisted.internet import reactor, protocol
from twisted.protocols import basic
from fileIndexing import search

class RequestHandlerProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.peer = self.transport.getPeer().host
        print("REQUEST HANDLER : Incoming Request From :"
              + self.peer)
        self.sendLine("Request Acknowledged..Processing")
    
    def connectionLost(self,reason):
        pass
    
    def lineReceived(self, line):
        self.result = search.search(line)
        if(self.result):
            print("File Found, Building Descriptor")
            desc_path = search.buildDescriptor(self.result)
            desc_file = open(desc_path,'rb')
            self.sendLine("REQUEST HANDLER:File Found..Sending Descriptor")
            self.setRawMode() 
            self.transport.write(desc_file.read())
            self.transport.write('\r\n')
            desc_file.close()
            self.setLineMode()
            self.sendLine("REQUEST HANDLER : Descriptor Sent")
            self.transport.loseConnection()
        else:
            self.sendLine("REQUEST HANDLER : No Such File Found..") 
            self.loseConnection()                  

class RequestHandlerFactory(protocol.ServerFactory):
    protocol = RequestHandlerProtocol
    
    def __init__(self):
        pass
    def buildProtocol(self, addr):
        return RequestHandlerProtocol()
    
def startRequestHandler():
    reactor.listenTCP(9890, RequestHandlerFactory())
    print("REQUEST HANDLER STARTED")

