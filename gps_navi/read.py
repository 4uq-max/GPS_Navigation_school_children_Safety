import pickle

pickle_in = open("h2t.pickle","rb")
example_dict = pickle.load(pickle_in)
print example_dict
print type(example_dict)
