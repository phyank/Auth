import pickle

WORD=0
CLASS=1
NO=2
CLASS_SUM=3

CURRENT_CLASS=0
WORD_COUNTER_DICT=1
SUM_OF_CLASS=2

CLASS_PARTICIPATION=0
DIMENSION=1
MEMBERS=2

#这个函数返回上述被pickle的字典
def get_cut_dataset():
    with open('data/pickle/cut_dataset.pickle','rb') as dumpfile:
        cut_dataset=pickle.load(dumpfile)
    return cut_dataset

def get_dict():
    with open('data/pickle/dict.pickle','rb') as pfile:
        dict=pickle.load(pfile)

    return dict

def make_class_dict(dict):
    class_dict={}
    for word in dict:
        current_class=dict[word][CLASS]
        if current_class not in class_dict:
            class_dict[current_class]=[0,1,''] #class_participation, sum_of_class_member
        else:
            class_dict[current_class][DIMENSION]+=1

    return class_dict