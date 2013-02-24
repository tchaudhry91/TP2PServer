from twisted.internet import reactor, protocol
from twisted.protocols import basic

class ListingServerProtocol(basic.LineReceiver):
    
    def __init__(self):
        self.gotListing = False
        self.peer = None
        self.user = None
        self.handler = None
        
    def connectionMade(self):
        self.peer = self.transport.getPeer().host
        print("LISTING SERVER : Got incoming connection from "
               + self.peer)
        self.transport.write('LISTING SERVER:Connected..')
    
    def connectionLost(self, reason):
        print("LISTING SERVER : Connection Terminated to "
              + self.peer)
        if self.gotListing:
            print("LISTING SERVER : Received Listing from"+
                  self.peer)
    
    def lineReceived(self, line):
        if line.startswith("ListingSendRequest"):
            self.setUserAndOpenHandler(line)            
            self.setRawMode()
            self.sendLine("proceed")
        else:
            print("Received Invalid Command from " + self.peer)
            self.transport.write("InvalidCommand")
    
    def rawDataReceived(self, data):
        if data.endswith('/r/n'):
            data = data[:-2]
            self.handler.write(data)
            self.handler.close()
            self.setLineMode()
            self.sendLine("LISTING SERVER : Received Listing")
            self.gotListing = True        
        else:
            self.handler.write(data)            
            
    def setUserAndOpenHandler(self, line):
        self.user = line.split(' ')[1]
        self.handler = open(self.user,'wb')            

class ListingServerFactory(protocol.ServerFactory):
    protocol = ListingServerProtocol
    
    def buildProtocol(self, addr):
        return ListingServerProtocol()
    
    def __init__(self):
        pass
    
def startListingServer():
    reactor.listenTCP(9880, ListingServerFactory())
    print("LISTING SERVER STARTED")
    
