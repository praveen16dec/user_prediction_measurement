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

## Can add as many parameters as you want to
param_1 = []
param_2 = []
param_3 = []
param_4 = []
# param_5 = []
# param_6 = []
# param_7 = []
# param_8 = []
# param_9 = []
# param_10 = []
target = []


for each in mea_fml[1:]:
    param_1.append(each[1])
    param_2.append(each[2])
    param_3.append(each[3])
    param_4.append(each[4])
    # param_5.append(each[5])
    # param_6.append(each[6])
    # param_7.append(each[7])
    # param_8.append(each[8])
    # param_9.append(each[9])
    # param_10.append(each[10])
    target.append(each[0])



param_list = [param_1, param_2, param_3, param_4]

comparator_dict = {}
measurements_match = {}

for i in range(3,5):
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
        #print(final_arr_trans_clean)
        
        ## Clustering of profiles with same input set and a tolerance of 1 in output
        for i, each in enumerate(final_arr_trans_clean):
            if list(each) not in measurements_match_list:
                measurements_match_list.append(list(each))
            for element in final_arr_trans_clean[i+1:,...]:
                if (list(each)[0:-1] == list(element)[0:-1]) and (abs(float(list(each)[-1])-float(list(element)[-1])) < 1 ):
                    if list(element) not in measurements_match_list:
                        measurements_match_list.append(list(element))
                    counter += 1
                elif (list(each)[0:-1] == list(element)[0:-1]) and (abs(float(list(each)[-1])-float(list(element)[-1])) > 1):
                    counter_not += 1
                else:
                    pass

        # for i, each in enumerate(final_arr_trans_clean):
        #     for element in final_arr_trans_clean[i+1:,...]:
        #         if list(each)[1:] == list(element)[1:] and list(each)[0] != list(element)[0]:
        #             counter_not += 1

                # counter_row = 0
                # for j in range(0,length-1):
                #     if (each[j] == element[j]):
                #         counter_row += 1
                # if counter_row == length-1 and each[-1] != element[-1]:
                #     counter_not += 1
 

        ## User profile list for different combination of input parameters
        for each in index_list:
            key = key + str(each) + "-"
            comparator_dict[key] = [counter, counter_not]
            measurements_match[key] = measurements_match_list


sorted_comparator_dict = sorted(comparator_dict.items(), key=lambda t: t[1][0])
#print(sorted_comparator_dict)

with open("match.json", 'w') as outfile:
    json.dump(measurements_match, outfile)



