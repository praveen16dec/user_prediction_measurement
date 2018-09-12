import numpy as np
import csv
import json
import itertools
import operator 

with open('/home/flyrobe/Documents/measurement/mea_ml_test.csv', 'r') as f:
    reader = csv.reader(f)
    mea_fml_test= list(reader)

error_dict = {}
accuracy_metric = {}
low_accuracy = {}
high_accuracy = {}
measurements_match = json.load(open('/home/flyrobe/Documents/measurement/match.json'))
test_1 = []
test_2 = []
test_3 = []
test_4 = []
test_5 = []
test_6 = []
test_7 = []
test_8 = []
test_9 = []
test_10 = []
test_11 = []
test_12 = []
test_target = []

for each in mea_fml_test[1:]:
    test_1.append(each[1])
    test_2.append(each[2])
    test_3.append(each[3])
    test_4.append(each[4])
    test_5.append(each[5])
    test_6.append(each[6])
    test_7.append(each[7])
    test_8.append(each[8])
    test_9.append(each[9])
    test_10.append(each[10])
    test_11.append(each[11])
    test_12.append(each[12])
    test_target.append(each[0])

test_param_list = [test_1, test_2, test_3, test_4, test_5, test_6, test_7, test_8, test_9, test_10, test_11, test_12]

for i in range(3,5):
    comb_list = list(itertools.combinations(test_param_list,i))
    for each in comb_list:
        counter_found = 0
        counter_match = 0
	counter_true = 0
        counter_total = 0
        test_key = ""
        test_list_1 = []
        test_index_list = []
        for element in each:
            test_index_list.append(test_param_list.index(element))
            test_list_1.append(element)
        test_list_1.append(test_target)

        test_final_arr = np.array(test_list_1)
        test_final_arr_trans = np.transpose(test_final_arr)

        test_index_list_new = []

        for index, each in enumerate(test_final_arr_trans):
            for element in each:
                if float(element) < 10 or float(element) > 60:
                    test_index_list_new.append(index)
        test_final_arr_trans_clean = np.delete(test_final_arr_trans,test_index_list_new,0)
        
	## Generating the combination of input parameters in the test data
	for each in test_index_list:
            test_key = test_key + str(each) + "-"
        
	for each in test_final_arr_trans_clean:
            counter_total += 1
	    try:
            	look_up_list = list(measurements_match[test_key])
	    except:
	        pass
	    low_accuracy[test_key] = {}
	    high_accuracy[test_key] = {}
	
        for element in test_final_arr_trans_clean:
	        low_accuracy[test_key][list(element)[-1]] = []
	        high_accuracy[test_key][list(element)[-1]] = []
            for each in look_up_list:
                if (list(each)[0:-1] == list(element)[0:-1]):
                    #counter_found += 1
		    ## Calculating the distance between the outputs for same input parameters in test_data
                    if test_key not in error_dict:
                        error_dict[test_key] = [[abs(float(list(element)[-1]) - float(list(each)[-1])),float(list(element)[-1])]]
                    else:
                        error_dict[test_key] += [[abs(float(list(element)[-1]) - float(list(each)[-1])),float(list(element)[-1])]]

		        if (abs(float(list(element)[-1]) - float(list(each)[-1])) > 2):
		            low_accuracy[test_key][list(element)[-1]].append(list(element)[0:-1])
		        else:
			        high_accuracy[test_key][list(element)[-1]].append(list(element)[0:-1])
        
	    for element in test_final_arr_trans_clean:
            for each in look_up_list:
                if (list(each)[0:-1] == list(element)[0:-1]):
                    if (abs(float(list(each)[-1]) - float(list(element)[-1])) <= 1):
                        counter_match += 1
                        break   
        for element in test_final_arr_trans_clean:
            for each in look_up_list:
                if (list(each)[0:-1] == list(element)[0:-1]):
                    counter_found += 1
                    break  
        accuracy_metric[test_key] = [counter_match, counter_found, counter_total]
        #error_dict[test_key] = counter_test
#print(error_dict)
#error_dict_avg = {}
#for each in error_dict:
    #sum = 0
    #count_avg = 0
    #for element in error_dict[each]:
        #sum += float(element[0])
        #count_avg += 1
    #error_dict_avg[each] = sum/count_avg

#print(error_dict_avg)
output_error = {}
for each in error_dict:
    output_error[each] = []
    for element in error_dict[each]:
        output_error[each].append(element[0])

for each in output_error:
    sum =0
    for value in output_error[each]:
        sum += value
    count = len(output_error[each])
    output_error[each] = sum/count

filename_1 = "low_accuracy.json"
filename_2 = "high_accuracy.json"
with open(filename_1, 'w') as outfile:
    json.dump(low_accuracy, outfile)


with open(filename_2, 'w') as outfile:
    json.dump(high_accuracy, outfile)


print(output_error)
print(accuracy_metric)
#print(low_accuracy)
#print(high_accuracy)


