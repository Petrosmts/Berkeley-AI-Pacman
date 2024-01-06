import os
from rlfa import *
import time
import threading


def grouping(): #this function matches the files depending on the name of each test. I found the reading from file functions with the os library in the Internet.
    content = list()
    var_list = list() #list with files with name var...
    dom_list = list() #list with files with name dom...
    ctr_list = list() #list with files with name ctr...
    dir = '/home/petrakis/ArtIn/RLFA/rlfap'
    if os.path.exists(dir) == True: 
        for name in os.listdir(dir) : 
            if name != "odigies.txt" and name[len(name) - 4 : len(name)] == ".txt": #we want to check only the txt files and NOT the odigies.txt
                with open(os.path.join(dir,name), 'r') as cur_file: 
                    content = cur_file.readlines() #content is a list where each line of cur_file is a list item.
                    if name[0] == 'v':
                        var_list.append((name, content))
                    elif name[0] == 'd':
                        dom_list.append((name, content))
                    elif name[0] == 'c':
                        ctr_list.append((name, content))
                    cur_file.close()
    else: 
        print("Error: Directory given is wrong!")
    group_list = list() #function will return this list.
    temp = " "
    for var,cont1 in var_list:
        sol1 = cont1
        temp = var[3:len(var)-4] #name of the test so we can match correctly the files.
        for dom,cont2 in dom_list:
            temp2 = "dom" + temp + ".txt"
            if dom == temp2: #if file dom has the same test name with file var then save the content and remove it from the dom files list.
                sol2 = cont2
                dom_list.remove((dom, cont2))
                break
        for ctr,cont3 in ctr_list:
            temp3 = "ctr" + temp + ".txt"
            if ctr == temp3: #if file ctr has the same test name with file var then save the content and remove it from the ctr files list.
                sol3 = cont3
                ctr_list.remove((ctr, cont3))
                break
        group_list.append((sol1, sol2, sol3, temp)) #put in the list a tuple with content of 3 files(var, dom, ctr) with the same test name and the test name itself.
    return group_list

def function_timeout():
    print("Time limit exceeded. Bye!")
    os._exit(1)

if __name__ == '__main__':
    group_list = grouping() #group correctly the files.
    print("Hey! Type one of the following test names to see this test's solution(if there is one)! All tests run with dom_wdeg function instead of mrv.")
    for var_name, dom_name, ctr_name, test_name in group_list:
        print(test_name) #print all test names.
    go_on = 'y'
    while go_on == 'y':
        timeout_thread = threading.Timer(500, function_timeout) #After 500 seconds, timeout.
        found = False
        name = input("Give me the test's name: ")
        for var_name, dom_name, ctr_name, test_name in group_list:
            if name == test_name: #if name given is the same with the test's name.
                found = True
                running_test = rlfa(var_name, dom_name, ctr_name) #create the object with class rlfa.
                alg1 = input("Type the name of the algorithm you want. fc or mac? ")
                timeout_thread.start()
                if alg1 == "fc":
                    start = time.time()
                    result = backtracking_search(running_test, dom_wdeg, unordered_domain_values, forward_checking_with_dom_wdeg)
                    end = time.time()
                    print(result,'\n')
                    print("Numbers of constraints checked:",running_test.ctrs_checked)
                    print("Time passed", round(end - start, 6), "seconds")
                elif alg1 == "mac":
                    start = time.time()
                    result = backtracking_search(running_test, dom_wdeg, unordered_domain_values, mac_with_dom_wdeg)
                    end = time.time()
                    print(result,'\n')
                    print("Numbers of constraints checked:",running_test.ctrs_checked)
                    print("Time passed", round(end - start, 6), "seconds")
                else:
                    print("Name you gave is not valid.")
        timeout_thread.cancel() 
        if found == False: #if name given doesn't belong to any test.
            print("Wrong input! Try again!")   
        go_on = input("\nWant to check more tests? Press y for YES or anything else for NO: ")   