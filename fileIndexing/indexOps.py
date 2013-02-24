from . import fl_class
import pickle

def addNewListing(new_listing):
    fl_input = open(new_listing, "rb")
    fl_object = pickle.load(fl_input)
    print(fl_object.getOpenFiles())
    print("Listing Added")