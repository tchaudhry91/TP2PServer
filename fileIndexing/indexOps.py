import fl_class
import pickle

def addNewListing(new_listing, ip_add):
    fl_input = open(new_listing, "rb")
    fl_object = pickle.load(fl_input)
    fl_input.close()
    fl_output = open(new_listing,'wb')
    fl_object.setIp(ip_add)
    pickle.dump(fl_object,fl_output)
    print("Listing Added")