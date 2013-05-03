from fileIndexing import indexOps
from listingListener import listingServer
from twisted.internet import reactor
from requestHandler import requestHandler
from fileListing import utilities
import os

if __name__=="__main__":
    if os.path.exists(os.path.join(os.getcwd(),'Listings')):
        utilities.cleanListings()
    else:
        os.mkdir(os.path.join(os.getcwd(),'Listings'))
    if os.path.exists(os.path.join(os.getcwd(),'Temp')):
        utilities.cleanTemps()
    else:
        os.mkdir(os.path.join(os.getcwd(),'Temp'))
    listingServer.startListingServer()
    requestHandler.startRequestHandler()    
    reactor.run()    
    
    