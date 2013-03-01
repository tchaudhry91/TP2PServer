from fileIndexing import indexOps
from listingListener import listingServer
from twisted.internet import reactor
from requestHandler import requestHandler

if __name__=="__main__":
    listingServer.startListingServer()
    requestHandler.startRequestHandler()    
    reactor.run()    
    