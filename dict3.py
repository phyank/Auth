import jieba.posseg
import csv
import pickle

#这个列表存储目标CSV文件的名称。要添加新的文件，只需加在此处。
database=['dsjwz.csv','gkw.csv','jqzx.csv','ktx.csv','mm.csv','xkd.csv','xsx.csv']

# 这个函数解析上述列表里的CSV文件，并返回一个字典。字典的键为上面列表里的名称，对应的值是每个csv文件的文章列表。
# 其中每一篇文章是一个元组：（num,url,title,content）
def make_original_dataset():
    original_dataset={}

    for acsv in database:
        original_dataset[acsv]=[]

        with open('data/'+acsv) as csvfile:
            reader=csv.DictReader(csvfile)
            for aline in reader:
                (original_dataset[acsv]).append((aline['num'],aline['url'],aline['title'],aline['content']))

    return original_dataset

#这个函数将哈工大同义词林转换为一个python字典，并返回。
def make_dict():

    wordlist = open('hlp_ll.txt', 'rb').readlines()

    decodedwl = []

    dict = {}

    for line in wordlist:
        decodedwl.append(line.decode("GBK"))

    father = ''
    for line in decodedwl:
        if '=' in line:
            line = line.split(" ")[1:]
            line[-1] = line[-1][:-2]
            father = line[0]

            i = 0
            for word in line:
                dict[word] = [word, father, i]

    return dict

#这个函数将传入字符串中的实词提取出，并返回包含这些实词的字符串，词以空格分隔。
def get_real_words(str1):
        seg = jieba.posseg.cut(str1)
        punc = open("punctuation.txt", 'rb')
        pr = punc.read()
        pr = pr.decode('gbk')
        p = pr.split()
        lreal = []
        lvir = []
        punclist = ["，", ",", "“", "”", "‘", "’", ".", "。", ":", "：", ";", "；", "！",
                    "!", "？", "?", "（", "）", "(", ")", '、', '——', '《', '》', '…', "……"]
        passlist = ['\\', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", '/', '-', '$', '#']
        puncreplace = ["逗号", "逗号", "引号", "引号", "引号", "引号", "句号", "句号", "冒号",
                       "冒号", "分号", "分号", "感叹号", "感叹号", "问号", "问号", "括号",
                       "括号", "括号", "括号", '顿号', '破折号', '书名号', '书名号', '省略号', "省略号"]
        for i in seg:
            if i.word in passlist:
                pass
            elif i.word in punclist:
                for j in range(len(punclist)):
                    if i.word == punclist[j]:
                        lvir.append(puncreplace[j])
            elif i.flag in ['n', 'v', 'a'] and i.word not in p:
                lreal.append(i.word)
            # elif i.flag not in ['eng'] and i.word in p:
            #     lvir.append('填充' + i.word)
        strreal = " ".join(lreal)
        return strreal

#这个函数没有返回值，它将database列表里的所有csv文件进行分词，并生成两个集合：
#   1. 与每个csv文件对应的实词词袋，放置于同一个文件夹中，文件名为： csv文件名+‘.txt’
#   2. 一个记录所有csv文章各自的实词的字典，它的结构与上面提到的original_dataset字典一样，
#       只不过文章的content是这篇文章中实词的字符串。这个词典被pickle到cut_dataset.pickle
#       中，方便再次读取
def make_cut():
    original_dataset = make_original_dataset()
    cut_dataset={}

    for acsv in database:
        real_words=''
        cut_dataset[acsv]=[]
        current_list=cut_dataset[acsv]
        for article in original_dataset[acsv]:
            current_real_words=get_real_words(article[3])
            real_words+=current_real_words
            current_list.append((article[0],article[1],article[2],current_real_words))


        file=open('data/cut/'+acsv+'.txt','w')
        file.write(real_words)
        file.close()
        print('Cutting '+acsv+' completed!')

    file = open('data/pickle/cut_dataset.pickle', 'wb')
    pickle.dump(cut_dataset,file,2)
    file.close()
    print("Dumping cut dataset success!")

#这个函数返回上述被pickle的字典
def get_cut_dataset():
    with open('data/pickle/cut_dataset.pickle','rb') as dumpfile:
        cut_dataset=pickle.load(dumpfile)
    return cut_dataset

def run(learnlist,checklist,dict):
    counterl={}
    counterc={}

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

            difference+=(ratio1-ratio2 if ratio1>=ratio2 else ratio2-ratio1)

    return difference/sum,sum,len(common_class)

dict=make_dict()

for i in range(0,len(database)):
    for j in range(i+1, len(database)):

        with open('data/'+database[i]+'.txt') as file1:
            list1=file1.read().split()

        with open('data/'+database[j]+'.txt') as file2:
            list2=file2.read().split()

        index,sum1,sum2=run(list1,list2,dict)
        print('learn:',database[i],', check:',database[j],' \t',' Result:',' \t',index,' \t',sum1,' \t',sum2)
