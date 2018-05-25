import pickle

def reecode():
    with open('hlp_ll.txt','rb') as file:
        data=file.read()

    data=data.decode('gbk')

    with open('hlp_ll_utf8','w') as ofile:
        ofile.write(data)

def t():
    with open('classes.txt','r') as f:
        lines=f.readlines()

    records=[]
    for line in lines:
        line=line.split()
        record=[line[0],float(line[1][3:]),int(line[2][4:])]
        records.append(record)

    records=sorted(records,key=lambda tuple: tuple[1]/tuple[2],reverse=True)

    print(len(records))

    records=records[3000:]
    print(len(records))
    pass_dict={}
    for record in records:
        pass_dict[record[0]]=True

    with open('data/pickle/pass_dict.pickle','wb') as p:
        pickle.dump(pass_dict,p,2)




t()