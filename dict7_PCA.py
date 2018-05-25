from Auth.common import *
#from Auth.parse_and_cut import *

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#import matplotlib


import numpy as np

#同义词类内部词频差异比较
vector_class=[]

with open('classes.txt', 'r') as f:
    lines = f.readlines()

records = []
for line in lines:
    line = line.split()
    record = [line[0], float(line[1][3:]), int(line[2][4:])]
    records.append(record)

records = sorted(records, key=lambda tuple: tuple[1], reverse=True)

for record in records:
    className=record[0]
    vector_class.append(className)


def get_vector(dict,class_member_dict,countDict,dimension=1000):
    vector=[]

    i=0
    for className in vector_class:
        try:
            wordCounter=countDict[className][WORD_COUNTER_DICT]
        except:
            class_record=class_member_dict[className]
            for j in range(0,len(class_record)):
                vector.append(0)
                i+=1
                if i >= dimension: break
        else:
            classSum=countDict[className][SUM_OF_CLASS]
            for wordName in class_member_dict[className]:
                try:
                    wordSum=wordCounter[wordName]
                except:
                    wordSum=0

                i+=1
                vector.append(wordSum/classSum)
                if i>=dimension: break

        if i>=dimension: break
    return vector

def run_single(wordList,dict):
    counterl = {}

    for word in wordList:
        if word not in dict:
            pass
        else:
            record = dict[word]

            current_class = record[CLASS]

            if current_class not in counterl:
                counterl[current_class] = [current_class, {word: 1}, 1]
                continue
            else:
                if word in counterl[current_class][WORD_COUNTER_DICT]:
                    counterl[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterl[current_class][WORD_COUNTER_DICT][word] = 1

                counterl[current_class][SUM_OF_CLASS] += 1

    return counterl

def run(learnlist,checklist,dict):
    counterl={}
    counterc={}
    class_dict=make_class_dict(dict)

    for word in learnlist:
        if word not in dict:
            pass
        else:
            record=dict[word]

            current_class=record[CLASS]

            if current_class not in counterl:
                counterl[current_class]=[current_class,{word:1},1]
                continue
            else:
                if word in counterl[current_class][WORD_COUNTER_DICT]:
                    counterl[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterl[current_class][WORD_COUNTER_DICT][word] = 1

                counterl[current_class][SUM_OF_CLASS]+=1

    for word in checklist:
        if word not in dict:
            pass
        else:
            record = dict[word]

            current_class = record[CLASS]

            if current_class not in counterc:
                counterc[current_class] = [current_class, {word: 1}, 1]
                continue
            else:
                if word in counterc[current_class][WORD_COUNTER_DICT]:
                    counterc[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterc[current_class][WORD_COUNTER_DICT][word] = 1

                counterc[current_class][SUM_OF_CLASS] += 1

    common_class={}

    for aClass in counterl:
        if aClass in counterc:
            common_class[aClass]=True

    difference=0
    sum=0

    for aClass in common_class:
        difference_counter={}
        class_record_l=counterl[aClass]
        word_counter_dict_l=class_record_l[WORD_COUNTER_DICT]

        class_record_c = counterc[aClass]
        word_counter_dict_c=class_record_c[WORD_COUNTER_DICT]

        for aWord in word_counter_dict_l:
            difference_counter[aWord]=True

        for aWord in word_counter_dict_c:
            difference_counter[aWord]=True

        for aWord in difference_counter:
            sum+=1

            if aWord in word_counter_dict_l:
                ratio1=word_counter_dict_l[aWord]/class_record_l[SUM_OF_CLASS]
            else:
                ratio1=0

            if aWord in word_counter_dict_c:
                ratio2 = word_counter_dict_c[aWord] / class_record_c[SUM_OF_CLASS]
            else:
                ratio2 = 0

            if not ratio1:
                appear='B'
            elif not ratio2:
                appear='A'
            else:
                appear='AB'

            abs=ratio1-ratio2 if ratio1>=ratio2 else ratio2-ratio1

            class_dict[aClass][CLASS_PARTICIPATION]+=abs

            class_dict[aClass][MEMBERS]+=' '+aWord+appear+str(abs)

            difference+=abs

    if sum!=0:
        return difference/sum,sum,len(common_class),class_dict
    else:
        return 0,sum,len(common_class),class_dict


def com_all():

    dict=get_dict()


    for i in range(0,len(database)):
        for j in range(i+1, len(database)):

            with open(CUT_FILE_DIR+database[i]+'.txt') as file1:
                list1=file1.read().split()

            with open(CUT_FILE_DIR+database[j]+'.txt') as file2:
                list2=file2.read().split()

            index,sum1,sum2,class_dict=run(list1,list2,dict)

            sorted_class=[]
            for key in class_dict:
                class_record=class_dict[key]
                sorted_class.append((key,class_record[CLASS_PARTICIPATION],class_record[DIMENSION],class_record[MEMBERS]))


            sorted_class=sorted(sorted_class,key=lambda tuple: tuple[1],reverse=True)

            result='learn:'+database[i]+' check:'+database[j]+' \t Result: \t'+str(index)+' \t'+str(sum1)+' \t'+str(sum2)
            print(result)

            result+='\n\n\n'
            l=0
            for k in sorted_class:
                if l<=1000:
                    if k[1]:
                        result+="\n  \tclass: "+k[0]+"  \td: "+str(k[2])+"  \tpt: "+str(k[1])+"  \tdiff: "+k[3]
                        l+=1
                else:
                    break
            rfile=open('data/result/'+str(i)+' v. '+str(j)+'.txt','w')
            rfile.write(result)
            rfile.close()

def cmp_article(learn_set,check_set,list_of_article):
    dict=get_dict()

    with open(CUT_FILE_DIR + learn_set + '.txt') as file1:
        list1 = file1.read().split()

    m=0###############
    sumindex=0########
    for article in list_of_article:
        list2=article[3].split()
        index, sum1, sum2, class_dict = run(list1, list2, dict)

        sorted_class = []
        for key in class_dict:
            class_record = class_dict[key]
            sorted_class.append(
                (key, class_record[CLASS_PARTICIPATION], class_record[DIMENSION], class_record[MEMBERS]))

        sorted_class = sorted(sorted_class, key=lambda tuple: tuple[1], reverse=True)


        title=article[2]
        title=title.replace('/','div')
        title=title.replace('.','point')

        result = '\tlearn:' + learn_set + ' check '+check_set+":"+article[0]+':' + title + '     \t Result: \t' + str(index) + ' \t' + str(
            sum1) + ' \t' + str(sum2)

        sumindex+=index######################
        if index:
            m+=1#################################

        print(result)

        result += '\n\n\n'
        l = 0
        for k in sorted_class:
            if l <= 1000:
                if k[1]:
                    result += "\n  \tclass: " + k[0] + "  \td: " + str(k[2]) + "  \tpt: " + str(k[1]) + "  \tdiff: " + k[3]
                    l += 1
            else:
                break
        rfile = open(CHK_ARTICLE_REPORT_DIR + learn_set + '.v.' + check_set+ ":"+article[0]+":"+title + '.txt', 'w')
        rfile.write(result)
        rfile.close()

    print("avg: ",sumindex/m)


def tt_run():
    dict = get_dict()

    # 极端情况测试——完全不同
    index, sum1, sum2, class_dict = run(['女巫', '女巫', '女巫'], ['巫婆'], dict)
    print('Different--- Result: \t' + str(index) + ' \t' + str(sum1) + ' \t' + str(sum2))

    # 极端情况测试——比较不同
    dict = get_dict()
    index, sum1, sum2, class_dict = run(['巫婆', '巫婆', '巫婆', '女巫'], ['巫婆', '女巫', '女巫', '女巫', '女巫'], dict)
    print('Vary--- Result: \t' + str(index) + ' \t' + str(sum1) + ' \t' + str(sum2))

    # 极端情况测试——比较类似
    dict = get_dict()
    index, sum1, sum2, class_dict = run(['女巫', '女巫', '女巫'], ['巫婆', '女巫', '女巫', '女巫', '女巫'], dict)
    print('Alike--- Result: \t' + str(index) + ' \t' + str(sum1) + ' \t' + str(sum2))

    # 极端情况测试——完全相同
    dict = get_dict()
    index, sum1, sum2, class_dict = run(['女巫', '女巫'], ['女巫', '女巫', '女巫', '女巫', '女巫', '女巫'], dict)
    print('Same--- Result: \t' + str(index) + ' \t' + str(sum1) + ' \t' + str(sum2))

cut_dataset=get_cut_dataset()

listofa=cut_dataset['xsx.csv']
listofa2=cut_dataset['mm.csv']
#cmp_article('jqzx.csv','jqzx.csv',listofa)
#test_run()
l1=len(listofa)
l2=len(listofa2)
print(l1,' ',l2)
listofa=listofa+listofa2

dict=get_dict()
class_member_dict=make_class_member_dict(dict)

listofv=[]
for article in listofa:
    list=article[3].split()
    countDict=run_single(list,dict)
    vector=get_vector(dict,class_member_dict,countDict,2000)
    listofv.append(vector)

listofv=np.array(listofv)
pca=PCA(n_components=30)
print('Start transform')
newdata=pca.fit_transform(listofv)


estimator = KMeans(n_clusters=20)#构造聚类器
estimator.fit(newdata)

index=0
inner_index=0
labeldict={}
for label in estimator.labels_:
    if inner_index==l1: inner_index=0
    if index<l1:
        class_name='xsx'
    else:
        class_name='mm'

    try:
        record=labeldict[label]
    except:
        labeldict[label]=[]

    labeldict[label].append((class_name,inner_index))
    index+=1
    inner_index+=1

for label in labeldict:
    print(label,'-------------------------------------------------------')
    for item in labeldict[label]:
        print(item[0],item[1])







