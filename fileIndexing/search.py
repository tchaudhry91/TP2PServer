import os
import pickle
import fl_class

def search(file_name):
    tup = os.walk(os.path.join(os.getcwd(),'Listings'))
    files = tup[2]
    for listing in files:
        fl_class_obj = pickle.load(open(os.path.join(
                        os.getcwd(),'Listings',listing),'rb'))
        file_list = fl_class_obj.getOpenFiles()
        for current_file in file_list:
            if current_file == file_name:
                return (current_file, fl_class_obj.getIp())
        