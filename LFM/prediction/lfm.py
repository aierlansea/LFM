#-*-coding:utf-8-*-
import numpy as np

import sys
sys.path.insert(0,"G:\\recommedation\\LFM\\util")

import util.read as read
import operator
def lfm_train(train_data,F,alpha,beta,step):
    user_vec = {}
    item_vec = {}
    for step in range(step):
        for data_instance in train_data:
            userid,itemid,label=data_instance
            if userid not in user_vec:
                user_vec[userid]=init_model(F)
            if itemid not in item_vec:
                item_vec[itemid]=init_model(F)
        delta=label-model_prediction(user_vec[userid],item_vec[itemid])
        for index in range(F):

            user_vec[userid][index]+=beta*(delta*item_vec[itemid][index]-alpha*user_vec[userid][index])
            item_vec[itemid][index]+=beta*(delta*user_vec[userid][index]-alpha*item_vec[itemid][index])
        beta=beta*0.9
    return user_vec,item_vec
def init_model(vetor_len):
    return np.random.randn(vetor_len)

def model_prediction(user_vector,item_vector):
    res=np.dot(user_vector,user_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
    return res
def model_train_process():
    train_data=read.get_train_data("../data/ratings.txt")
    user_vector, item_vector=lfm_train(train_data,50,0.01,0.1,50)
    # print (user_vector[20])
    # print (item_vector['157'])
    for userid in user_vector:
        recom_result= (get_recomend_result(user_vector,item_vector,userid))
        #ana_recommendation_result(train_data,userid,recom_result)
def get_recomend_result(user_vec,item_vec,userid):
    if userid not in  user_vec:
        print ("kong")
        return []
    fix_num=10
    record={}
    recon_list=[]
    user_vector=user_vec[userid]
    for itemid in item_vec:
        item_vector=item_vec[itemid]
        res=np.dot(user_vector,item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
        record[itemid]=res
    for zuhe in sorted(record.iteritems(),key=operator.itemgetter(1),reverse=True)[:fix_num]:
        itemid=zuhe[0]
        score=round(zuhe[1],3)
        recon_list.append((itemid,score))
    return recon_list

def ana_recommendation_result(train_data,userid,reconlist):
    item_info=read.get_info("../data/movies.txt")
    for data_distance in train_data:
        tmp_userid,itemid,label=data_distance
        if tmp_userid==userid and label==1:
            print (item_info[itemid])
    print("recom result")
    for zuhe in reconlist:
        print (item_info[zuhe[0]])
if __name__=="__main__":
    model_train_process()

