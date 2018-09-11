import csv
import numpy as np
import json

with open('/Users/praveenyadav/Downloads/reverse_engineering.csv', 'r') as f:
    reader = csv.reader(f)
    rev_eng = list(reader)

param_1 = []
param_2 = []
param_3 = []
param_4 = []
param_5 = []
param_6 = []
param_7 = []
param_8 = []
param_9 = []
param_10 = []
target = []

for each in rev_eng[1:]:
    param_1.append(each[1])
    param_2.append(each[2])
    param_3.append(each[3])
    param_4.append(each[4])
    param_5.append(each[5])
    param_6.append(each[6])
    param_7.append(each[7])
    param_8.append(each[8])
    param_9.append(each[9])
    param_10.append(each[10])
    target.append(each[-1])

param_list = [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11, param_12, param_13, param_14]

user_dict = {}

for each in rev_eng[1:]:
    if each[-1] not in user_dict:
        user_dict[each[-1]] = [each[1:-1]]
    else:
        user_dict[each[-1]].append(each[1:-1])


for each in user_dict:
    user_dict[each] = np.transpose(np.array(user_dict[each]))
#print(user_dict)

for each in user_dict:
    for element in user_dict[each]:
        for value in element:
            if float(value) < 10 or float(value) > 60:
                list(element).remove(value)
maths_dict = {}
for each in user_dict:
    maths_dict[each] = {}
    for i, element in enumerate(user_dict[each]):
        maths_dict[each][i] = {}
        mean = np.mean((np.array(element)).astype(float))
        variance = np.var((np.array(element)).astype(float))
        # for value in element:
        #     sum = sum + float(value)
        #     count += 1
        # mean = sum/count
        # diff = 0
        # for item in element:
        #     diff = diff + (float(value) - float(mean))*(float(value) - float(mean))
        # try:
        #     variance = diff/(count-1)
        # except ZeroDivisionError:
        #     pass
        maths_dict[each][i]["mean"] = mean
        maths_dict[each][i]["variance"] = variance

#print(maths_dict)
with open('data_mean.json', 'w') as outfile:
    json.dump(maths_dict, outfile)

variance = {}

for each in maths_dict:
    for obj in maths_dict[each]:
        if obj not in variance:
            variance[obj] = [maths_dict[each][obj]["variance"]]
        else:
            variance[obj].append(maths_dict[each][obj]["variance"])

print(variance)
mean_variance = {}

for each in variance:
    mean_variance[each] = np.mean(np.array((variance[each])))

sorted_mean_variance = sorted(mean_variance.items(), key=lambda t: t[1])
print(sorted_mean_variance)


