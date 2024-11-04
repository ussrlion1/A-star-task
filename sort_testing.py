from statistics import mode, median, mean, stdev
from db_for_a_star_task import db

db = db('db_for_a_star_task.db')

tests = db.get_results()
number_of_passed_tests = 0
number_of_failed_tests = 0
a_star_arr=[]
backtracking_arr=[]
has_way = lambda x: x!=-1
for i in range(len(tests)):
    a_star = [tests[i][0], tests[i][1]]
    backtracking = [tests[i][2], tests[i][3]]
    if a_star[0]== -1 and backtracking[0]== -1: number_of_failed_tests += 1
    if (a_star[0] == backtracking[0]):
        number_of_passed_tests+=1
        a_star_arr.append(float(a_star[1]))
        backtracking_arr.append(float(backtracking[1]))

a_star_arr.sort()
backtracking_arr.sort()

print("Passed tests: ", number_of_passed_tests, "Failed tests: ", number_of_failed_tests)
print("Standart deviation: ", stdev(a_star_arr ), stdev(backtracking_arr ))
print ("Mean: ",mean(a_star_arr ), mean(backtracking_arr ))
print("Median: ",median(a_star_arr ), median(backtracking_arr ))
print("Mode: ",mode(a_star_arr ), mode(backtracking_arr ))

db.close()
"""
Standart deviation:  0.02148617061748219 0.02987836604657144
Mean:  0.04949364995044727 0.08146589212599942
Median:  0.04398608207702637 0.07887768745422363
Mode:  0.0362396240234375 0.043488502502441406
"""