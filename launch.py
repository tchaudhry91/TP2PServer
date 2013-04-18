from fileIndexing import indexOps
from listingListener import listingServer
from twisted.internet import reactor
from requestHandler import requestHandler
from fileListing import utilities

if __name__=="__main__":
    utilities.cleanListings()
    utilities.cleanTemps()
    listingServer.startListingServer()
    requestHandler.startRequestHandler()    
    reactor.run()    
    
    