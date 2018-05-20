with open('hlp_ll.txt','rb') as file:
    data=file.read()

data=data.decode('gbk')

with open('hlp_ll_utf8','w') as ofile:
    ofile.write(data)
