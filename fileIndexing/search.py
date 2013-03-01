import os
import pickle
import fileListing.descriptor
from fileListing.descriptor import Descriptor

def search(file_name):
    tup = os.walk(os.path.join(os.getcwd(),'Listings'))
    tup = tup.next()
    files = tup[2]
    for listing in files:
        fl_class_obj = pickle.load(open(os.path.join(
                        os.getcwd(),'Listings',listing),'rb'))
        file_list = fl_class_obj.getOpenFiles()
        for current_file in file_list:
            if current_file == file_name:
                return (current_file, fl_class_obj.getIp())
    else:
        return None
    
def buildDescriptor(tup):
    desc = Descriptor(tup[0],tup[1])
    desc_file = open(tup[0]+'.desc','wb')
    pickle.dump(desc,desc_file)
    desc_file.close()
    return tup[0]+'.desc'
    
        