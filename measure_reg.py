__author__ = 'py'


import numpy as np
from sklearn import linear_model
import csv
import itertools
from sklearn import preprocessing
import operator
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score
#from sklearn.model_selection

with open('/Users/praveenyadav/Downloads/mea_ml_train.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml = list(reader)

with open('/Users/praveenyadav/Downloads/mea_ml_test.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml_test = list(reader)

param_1 = []
param_2 = []
param_3 = []
param_4 = []
train_target = []


test_param_1 = []
test_param_2 = []
test_param_3 = []
test_param_4 = []
test_target = []
# print('Variance score: %.2f' % r2_score(np_test_y, data_y_pred))

## Can add as many parameters as you like. In this case, I have worked on four parameters
for each in mea_fml[1:]:
    param_1.append(each[1])
    param_2.append(each[2])
    param_3.append(each[3])
    param_4.append(each[4])
    train_target.append(each[0])


for each in mea_fml_test[1:]:
    test_param_1.append(each[1])
    test_param_2.append(each[2])
    test_param_3.append(each[3])
    test_param_4.append(each[4])
    test_target.append(each[0])


# np_train_target_clean = np_train_target[(int(np_train_target) > 13 and int(np_train_target) < 24)]
# np_train_target_clean_scaled = preprocessing.scale(np_train_target_clean)

param_list = [param_1, param_2, param_3, param_4]
test_param_list = [test_param_1, test_param_2, test_param_3, test_param_4]


## Regression on combination of 3 or 4 of parameters. This can be modified as per use.
error_dict = {}
for i in range(3,5):
    comb_list = list(itertools.combinations(param_list,i))
    for each in comb_list:
        list_1 = []
        list_2 = []
        index_list = []
        #csvfile = '/Users/py/Downloads/comb_new.csv'
        for element in each:
            index_list.append(param_list.index(element))
            list_1.append(element)
            #list_2.append(element[100:150])
        list_1.append(train_target)

        for each in index_list:
            list_2.append(test_param_list[each])
        list_2.append(test_target)

        np_train_arr = np.array(list_1)
        np_train_trans_arr = np.transpose(np_train_arr)
        np_test_arr = np.array(list_2)
        np_test_trans_arr = np.transpose(np_test_arr)
        #print(np_train_arr)
        #print(np_test_arr)
        
        ## Deleting the corrupt/fake data
        corrupt_index_list_train = []
        corrupt_index_list_test = []
        for index_train, each in enumerate(np_train_trans_arr):
            for element in each:
                if float(element) < 10 or float(element) > 60:
                    corrupt_index_list_train.append(index_train)
                    break

        np_train_clean = np.delete(np_train_trans_arr, corrupt_index_list_train, 0)

        for index_test, each in enumerate(np_test_trans_arr):
            for element in each:
                if float(element) < 10 or float(element) > 60:
                    corrupt_index_list_test.append(index_test)
                    break
        np_test_clean = np.delete(np_test_trans_arr, corrupt_index_list_test, 0)

        np_train_x = np_train_clean[..., 0:-1]
        np_train_y = np_train_clean[..., -1]

        np_train_x = np_train_x.astype(float)
        np_train_y = np_train_y.astype(float)

        np_test_x = np_test_clean[..., 0:-1]
        np_test_y = np_test_clean[..., -1]

        np_test_x = np_test_x.astype(float)
        np_test_y = np_test_y.astype(float)
        
        ## Linear Regression model and summary statistics to get the best set of parameters evaluated on MSE
        regr = linear_model.LinearRegression()
        regr.fit(np_train_x, np_train_y)
        data_y_pred = regr.predict(np_test_x)
        #print('Coefficients: \n', regr.coef_)
        #print("Mean squared error: %.2f"
        #         % mean_squared_error(np_test_y, data_y_pred))
        key = " "
        for each in index_list:
            key = key + str(each) + "-"
        error_dict[key] = mean_squared_error(np_test_y, data_y_pred)
        # #error_dict[key] = mean_absolute_error(np_test_y, data_y_pred)
        # #error_dict[key] = mean_squared_log_error(np_test_y, data_y_pred)
        # #error_dict[key] = explained_variance_score(np_test_y,data_y_pred)
        #error_dict[key] = mean_squared_log_error(np_test_y, data_y_pred)


sorted_error_dict = sorted(error_dict.items(), key=operator.itemgetter(1))
print(sorted_error_dict)







