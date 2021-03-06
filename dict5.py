from Auth.common import *
from Auth.parse_and_cut import *

#统计dict3测量方法中各个同义词类的贡献

def run(learnlist,checklist,dict,class_dict):
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

            # if not ratio1:
            #     appear='B'
            # elif not ratio2:
            #     appear='A'
            # else:
            #     appear='AB'

            abs=ratio1-ratio2 if ratio1>=ratio2 else ratio2-ratio1

            class_dict[aClass][CLASS_PARTICIPATION]+=abs

            class_dict[aClass][DIMENSION]+=1

            # class_dict[aClass][MEMBERS]+=' '+aWord+appear+str(abs)

            difference+=abs

    if sum!=0:
        return difference/sum,sum,len(common_class),class_dict
    else:
        return 0,sum,len(common_class),class_dict


def com_all():
    dict = get_dict()
    class_dict=make_class_dict(dict)

    for i in range(0,len(database)):
        for j in range(i+1, len(database)):

            with open(CUT_FILE_DIR+database[i]+'.txt') as file1:
                list1=file1.read().split()

            with open(CUT_FILE_DIR+database[j]+'.txt') as file2:
                list2=file2.read().split()


            index,sum1,sum2,class_dict=run(list1,list2,dict,class_dict)

            sorted_class=[]
            for key in class_dict:
                class_record=class_dict[key]
                sorted_class.append((key,class_record[CLASS_PARTICIPATION],class_record[DIMENSION],class_record[MEMBERS]))


            sorted_class=sorted(sorted_class,key=lambda tuple: tuple[1],reverse=True)

            result='learn:'+database[i]+' check:'+database[j]+' \t Result: \t'+str(index)+' \t'+str(sum1)+' \t'+str(sum2)
            print(result)

            # result+='\n\n\n'
            # l=0
            # for k in sorted_class:
            #     if l<=1000:
            #         if k[1]:
            #             result+="\n  \tclass: "+k[0]+"  \td: "+str(k[2])+"  \tpt: "+str(k[1])+"  \tdiff: "+k[3]
            #             l+=1
            #     else:
            #         break
            # rfile=open('data/result/'+str(i)+' v. '+str(j)+'.txt','w')
            # rfile.write(result)
            # rfile.close()

def cmp_article(cut_dataset):
    dict=get_dict()
    class_dict = make_class_dict(dict)

    for i in range(0,len(database)):

        learn_set= database[i]
        print('Start learing '+learn_set)
        with open(CUT_FILE_DIR + learn_set + '.txt') as file1:
            list1 = file1.read().split()

        list=[]
        for l in range(0,i):
            list.append(l)
        for l in range(i+1,len(database)):
            list.append(l)
        for j in list:
            check_set=database[j]

            list_of_article=cut_dataset[check_set]
            print('Start checking '+check_set)

            for article in list_of_article:
                list2=article[3].split()
                _, _, _, class_dict = run(list1, list2, dict,class_dict)

    sorted_class = []
    for key in class_dict:
        class_record = class_dict[key]
        sorted_class.append(
            (key, class_record[CLASS_PARTICIPATION], class_record[DIMENSION], class_record[MEMBERS]))

    print('Start sorting')
    sorted_class = sorted(sorted_class, key=lambda tuple: tuple[1], reverse=True)
    print('Sorting complete!')

    rfile = open('classes.txt', 'w')
    for record in sorted_class:
        rfile.write(record[0]+'   pt:'+str(record[1])+'    sum:'+str(record[2])+'\n')
    rfile.close()


cut_dataset=get_cut_dataset()
cmp_article(cut_dataset)





