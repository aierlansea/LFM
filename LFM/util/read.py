#-*-coding:utf-8-*-

import os

def get_info(input_file):
    itemId=[]
    title=[]
    genre=[]
    item_info={}
    if not os.path.exists(input_file):
        return {}

    fp=open(input_file)
    line_num=0
    for line_num in fp:
            if line_num ==0:
                line_num+=1
                continue
            tem=line_num.strip().split(',')

            if len(tem)<3:
                continue
            elif len(tem)==3:
                itemId=tem[0]
                title=tem[1]
                genre=tem[2]
            elif len(tem)>3:
                itemId=tem[0]
                genre=tem[-1]

                title=",".join(tem[1:-1])
            item_info[itemId]=[title,genre]
    fp.close()
    return item_info

def get_ave(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum=0
    record={}
    score={}
    fp=open(input_file)
    for line in fp:
        if linenum==0:
            linenum+=1
            continue
        item=line.strip().split(',')
        if len(item)<4:
            continue
        useid,itemId=int(item[0]),item[1]

        rating=float(item[2])

        if itemId not in record:
            record[itemId]=[0,0]

        record[itemId][0]+=1


        record[itemId][1]+=rating
    fp.close()
    for itemId in record:
        score[itemId]=round(record[itemId][1]/record[itemId][0],3)

    return score

def get_train_data(inputfile):
    if not os.path.exists(inputfile):

        return []
    linenum=0
    pos_dict={}
    neg_dict={}
    train_data=[]
    flo_score=4.0
    score_record=get_ave(inputfile)
    fp=open(inputfile)
    item=[]
    for line in fp:
        if linenum==0:
            linenum+=1
            continue
        item=line.strip().split(',')
        if len(item)<4:
            continue
        userid,itemid=int(item[0]),item[1]
        rating= float(item[2])

        if userid not in pos_dict:
                 pos_dict[userid]=[]

        if userid not in neg_dict:
            neg_dict[userid]=[]
        if rating >flo_score:
            pos_dict[userid].append((itemid,1))
        else:
            score=score_record.get(itemid,0)

            neg_dict[userid].append((itemid,score))
    fp.close()
    for userid in pos_dict:
        data_num=min(len(pos_dict[userid]),len(neg_dict.get(userid,[])))

        if data_num>0:
            train_data+=[(userid,zuhe[0],zuhe[1]) for zuhe in pos_dict[userid]][:data_num]


        else:
            continue
        sorted_list=sorted(neg_dict[userid],key=lambda element:element[1],reverse=True)[:data_num]
        train_data+=[(userid,zuhe[0],0) for zuhe in sorted_list]
        # if userid==1:
        #     print len(pos_dict[userid])
        #     print len(neg_dict[userid])
        #     print (sorted_list)
    return train_data




if __name__=='__main__':
    # item_dict=get_info("../data/movies.txt")
    # print (len(item_dict))
    #
    #
    # print (item_dict["1"])
    # print (item_dict["11"])
    # score_dict=get_ave("../data/ratings.txt")
    # print (len(score_dict))
    # print (score_dict["1"])
    train_data=get_train_data("../data/ratings.txt")
    print(train_data[270:300])













