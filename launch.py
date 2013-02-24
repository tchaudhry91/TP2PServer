from fileIndexing import indexOps
from listingListener import listingServer
from twisted.internet import reactor

if __name__=="__main__":
    listingServer.startListingServer()
    reactor.run()    
    