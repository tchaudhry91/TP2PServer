import os
import pickle
import fileListing.descriptor
from fileListing.descriptor import Descriptor

def listSearch(file_name):
    tup = os.walk(os.path.join(os.getcwd(),'Listings'))
    tup = tup.next()
    files = tup[2]
    results = []
    for listing in files:
        fl_class_obj = pickle.load(open(os.path.join(
                        os.getcwd(),'Listings',listing),'rb'))
        file_list = fl_class_obj.getOpenFiles()
        for current_file in file_list:
            if current_file == file_name:
                results.append((current_file, fl_class_obj.getUserName()))
    if results:
        path = buildSearchList(results)
        return path
    
    else:
        return None
    
def singleFileSearch(file_name, user):
    tup = os.walk(os.path.join(os.getcwd(),'Listings'))
    tup = tup.next()
    files = tup[2]
    for listing in files:
        fl_class_obj = pickle.load(open(os.path.join(
                        os.getcwd(),'Listings',listing),'rb'))
        file_list = fl_class_obj.getOpenFiles()
        for current_file in file_list:
            print("CurrentFile:"+current_file)
            print("User:"+user)
            print(fl_class_obj.getUserName())
            if current_file == file_name and fl_class_obj.getUserName() == user:
                return (current_file, fl_class_obj.getIp())
    return None
    
def buildSearchList(results):
    for i in range(100000):
        ind = 'temp'+str(i)+'.list'
        temp_file_str = os.path.join(os.getcwd(),'Temp',ind)
        if os.path.isfile(temp_file_str):
                    continue
        else:
            file_handler = open(temp_file_str,'wb')
            break
    pickle.dump(results, file_handler)
    file_handler.close()
    return temp_file_str    
    
def buildDescriptor(tup):
    desc = Descriptor(tup[0],tup[1])
    desc_file = open(tup[0]+'.desc','wb')
    pickle.dump(desc,desc_file)
    desc_file.close()
    return tup[0]+'.desc'
    
        