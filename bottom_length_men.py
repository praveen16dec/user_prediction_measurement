import csv
import numpy as np
import itertools
import operator
import json
from multiprocessing import Process
import  datetime
with open('/Users/praveenyadav/Downloads/mea_ml_train.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml = list(reader)


param_1 = []
#param_2 = []
#param_3 = []
#param_4 = []
target = []


for each in mea_fml[1:]:
    param_1.append(each[1])
    #param_2.append(each[2])
    #param_3.append(each[3])
    #param_4.append(each[4])
    # param_5.append(each[5])
    # param_6.append(each[6])
    # param_7.append(each[7])
    # param_8.append(each[8])
    # param_9.append(each[9])
    # param_10.append(each[10])
    target.append(each[0])


param_list = [param_1]#, param_2, param_3, param_4]

for i in range(1,2):
    comb_list = list(itertools.combinations(param_list,i))
    for each in comb_list:
        measurements_match_list = []
        key = ""
        list_1 = []
        index_list = []
        for element in each:
            index_list.append(param_list.index(element))
            list_1.append(element)
        list_1.append(target)
        length = len(list_1)

        final_arr = np.array(list_1)
        final_arr_trans = np.transpose(final_arr)
        counter = 0
        counter_not = 0
        index_list_new = []

        for index, each in enumerate(final_arr_trans):
            for element in each:
                if float(element) < 10 or float(element) > 60:
                    index_list_new.append(index)
        final_arr_trans_clean = np.delete(final_arr_trans,index_list_new,0)

        index_list_ratio = []
        ratio = []

        for ind, each in enumerate(final_arr_trans_clean):
            if float(each[-1])/float(each[0]) <0.4 or float(each[-1])/float(each[0]) > 0.7:
                index_list_ratio.append(ind)
        final_arr_trans_clean_ratio = np.delete(final_arr_trans_clean, index_list_ratio,0)

        for each in final_arr_trans_clean_ratio:
            ratio.append(float(each[-1])/float(each[0]))

            
import statistics as s
print(s.mean(ratio), s.variance(ratio), len(ratio))
print(ratio)

