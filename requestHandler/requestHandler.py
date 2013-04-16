from twisted.internet import reactor, protocol
from twisted.protocols import basic
from fileIndexing import search
import os

class RequestHandlerProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.peer = self.transport.getPeer().host
        print("REQUEST HANDLER : Incoming Request From :"
              + self.peer)
        self.sendLine("Request Acknowledged..Processing")
    
    def connectionLost(self,reason):
        pass
    
    def lineReceived(self, line):
        print(line)
        self.commands = line.split(' ')
        self.main_command = self.commands[0]
        self.file_name = self.commands[1]
        
        #Decide if Search Query or Descriptor Request
        if self.main_command == "search":
            self.searchQuery(self.file_name)
        elif self.main_command == "get":
            self.sendDescriptor(self.file_name,self.commands[2])
        
    def searchQuery(self, file_name):
        #Basic Search Query, Send Back List
        result = search.listSearch(file_name)
        if(result):
            print("Sending Search List now..")
            results_file = open(result,'rb')
            self.sendLine("REQUEST HANDLER:Files Found..Sending Search List")
            self.setRawMode() 
            self.transport.write(results_file.read())
            self.transport.write('\r\n')
            results_file.close()
            os.remove(result)
            self.setLineMode()
            self.sendLine("REQUEST HANDLER : Descriptor Sent")
            self.transport.loseConnection()
        else:
            self.sendLine("REQUEST HANDLER : No Such File Found..") 
            self.transport.loseConnection()     
    
    def sendDescriptor(self, file_name, user_name):   
        #Descriptor Request
        result = search.singleFileSearch(file_name, user_name)
        if(result):
            print("File Found, Building Descriptor")
            desc_path = search.buildDescriptor(result)
            desc_file = open(desc_path,'rb')
            self.sendLine("REQUEST HANDLER:File Found..Sending Descriptor")
            self.setRawMode() 
            self.transport.write(desc_file.read())
            self.transport.write('\r\n')
            desc_file.close()
            os.remove(desc_path)
            self.setLineMode()
            self.sendLine("REQUEST HANDLER : Descriptor Sent")
            self.transport.loseConnection()
        else:
            self.sendLine("REQUEST HANDLER : No Such File Found..") 
            self.transport.loseConnection()                  

class RequestHandlerFactory(protocol.ServerFactory):
    protocol = RequestHandlerProtocol
    
    def __init__(self):
        pass
    def buildProtocol(self, addr):
        return RequestHandlerProtocol()
    
def startRequestHandler():
    reactor.listenTCP(9890, RequestHandlerFactory())
    print("REQUEST HANDLER STARTED")

