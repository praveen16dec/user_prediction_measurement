import csv
import numpy as np
import pandas as pd
import json
from sklearn.model_selection import train_test_split

with open('/Users/praveenyadav/Downloads/mea_fml_train.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml_train = list(reader)

with open('/Users/praveenyadav/Downloads/mea_fml_test.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml_test = list(reader)

print(len(mea_fml_train))
print(len(mea_fml_test))


############################################### CLEANING OF DATA ###################################################
corrupt_data_index_train = []
corrupt_data_index_test = []

for index, each in enumerate(mea_fml_train[1:]):
    for element in each:
        if float(element) < 10 or float(element) > 70:
            corrupt_data_index_train.append(index+1)
            break
for index, each in enumerate(mea_fml_test[1:]):
    for element in each:
        if float(element) < 10 or float(element) > 70:
            corrupt_data_index_test.append(index+1)
            break

for each in sorted(corrupt_data_index_train, reverse=True):
    del mea_fml_train[each]
for each in sorted(corrupt_data_index_test, reverse=True):
    del mea_fml_test[each]

####################################### Generating User body profiles from train data ###############################
np_mea_fml_train = np.array(mea_fml_train[1:])
np_mea_fml_test  = np.array(mea_fml_test[1:])

print(np_mea_fml_train.shape, np_mea_fml_test.shape)

np_train_output = np_mea_fml_train[:,0]
np_train_input = np_mea_fml_train[:,1:]

np_test_output = np_mea_fml_test[:,0]
np_test_input = np_mea_fml_test[:,1:]

##################### Generating the frequency distribution of the user profiles and estimating the ################# 
############################## measures of central tendency on the range of output ##################################

counter = 0
user_profile_counter = {}
for i, each in enumerate(np_mea_fml_train[0:len(np_mea_fml_train)-1]):
    if str(each[1:]) not in user_profile_counter:
        user_profile_counter[str(each[1:])] = {"frequency" : 0, "output" : []}
        #user_profile_counter[str(each[1:])]["output"] = [each[0]]
        for element in np_mea_fml_train[i+1:]:
            if list(each[1:]) == list(element[1:]):
                counter += 1
                user_profile_counter[str(each[1:])]["frequency"] += 1
                user_profile_counter[str(each[1:])]["output"].append(element[0])

print(user_profile_counter)

for each in user_profile_counter:
    user_profile_counter[each]["output_mean"] = np.mean(np.array(user_profile_counter[each]["output"]))
    user_profile_counter[each]["output_variance"] = np.var(np.array(user_profile_counter[each]["output"]))

#################################### Estimating the user profile spread on the test data ############################
counter_total = 0
counter_find = 0
for i, each in enumerate(np_mea_fml_test[0:]):
    counter_total += 0
    for key, value in user_profile_counter.items():
        if str(each[1:]) == key:
            counter_find += 1
            break

print(counter_find, counter_total)








