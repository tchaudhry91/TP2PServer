from twisted.internet import reactor, protocol
from twisted.protocols import basic
from fileIndexing import indexOps
import os

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
        self.sendLine('LISTING SERVER:Connected..')
    
    def connectionLost(self, reason):
        print("LISTING SERVER : Connection Terminated to "
              + self.peer)
        if self.gotListing:
            print("LISTING SERVER : Received Listing from"+
                  self.peer)
            indexOps.addNewListing(os.path.join
                            ("Listings",self.user+".fls"), self.peer)
            
    def lineReceived(self, line):
        if line.startswith("ListingSendRequest"):
            print("LISTING SERVER : Got Request from "+self.peer)
            self.setUserAndOpenHandler(line)            
            self.setRawMode()
            self.sendLine("proceed")
        else:
            print("Received Invalid Command from " + self.peer)
            self.transport.write("InvalidCommand")
    
    def rawDataReceived(self, data):
        print("Retreiving Listing..")
        if data.endswith('\r\n'):
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
        self.handler = open(os.path.join
                            ("Listings",self.user+".fls"),'wb')            

class ListingServerFactory(protocol.ServerFactory):
    protocol = ListingServerProtocol
    
    def buildProtocol(self, addr):
        return ListingServerProtocol()
    
    def __init__(self):
        pass
    
def startListingServer():
    if(os.path.isdir('Listings')):
        pass
    else:
        os.mkdir('Listings')
    reactor.listenTCP(9880, ListingServerFactory())
    print("LISTING SERVER STARTED")
    
