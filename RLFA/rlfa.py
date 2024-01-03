import os
from csp import *

class rlfa(CSP):
    def __init__(self, variables, domains, constraints):
        var_for_csp = [] #list with variables.
        dom_for_csp = {} #dictionary where the key is a variable and the element is a list with all possible values.
        neighs_for_csp = {} #dictionary where
        list_for_ctrs = [] #so we can know the symbol(> or =) for each constraint. This list will have tuples with each constraint properly seperated with function split.
        for index, var in enumerate(variables):
            if index > 0: #first element is the amount of variables, we don't want to check that.
                var_domain = var.split(" ") #variable is var_dom[0], domain is var_dom[1].
                var_for_csp.append(var_domain[0]) #put variable in list for the csp.__init__.
                neighs_for_var = [] #list with neighbors of each variable
                for ind_ex, dom in enumerate(domains):
                    if ind_ex > 0: #first element is the amount of domains, we don't want to check that.
                        if dom[0] == var_domain[1][0]: #if the variable's domain is the one we are examining.
                            tdom = dom.split(" ")
                            domain_size = int(tdom[1]) #second element of domain files is the amount of values each domain has.
                            tdom[domain_size + 1] = tdom[domain_size + 1].replace('\n','') #last element must not have \n in it.
                            dom_values = [tdom[i] for i in range(2, domain_size + 2)] #posible values for a variable are from the third element(which has index = 2) till the end
                            dom_for_csp[var_domain[0]] = dom_values
                for in_dex, ctr in enumerate(constraints):
                    if in_dex > 0: #first element is the amount of constraints, we don't want to check that.
                        tctr = ctr.split(" ")
                        tctr[len(tctr) - 1] = tctr[len(tctr) - 1].replace('\n','') #last element must not have \n in it.
                        cons = (tctr[0], tctr[1], tctr[2], tctr[3])
                        list_for_ctrs.append(cons)
                        if var_domain[0] == tctr[0]: #if the variable we are examining is the first variable in each constraint, then the second is neighbor of the first.
                            neighs_for_var.append(tctr[1])
                        elif var_domain[0] == tctr[1]: #if the variable we are examining is the second variable in each constraint, then the first is neighbor of the second.
                            neighs_for_var.append(tctr[0])
                neighs_for_csp[var_domain[0]] = neighs_for_var
                self.list_for_ctrs = list_for_ctrs
            super().__init__(var_for_csp, dom_for_csp, neighs_for_csp, self.f) #calling the CSP class init function with super().__init__ giving the necessary arguments.


    def f(self, A, a, B, b): #constraint function
        for var1, var2, symbol, k in self.list_for_ctrs: 
            if (var1 == A and var2 == B) or (var1 == B and var2 == A): #variables might be given with the wrong order.
                if symbol == '>':
                    if abs(int(a)-int(b)) > int(k):
                        return True
                elif symbol == '=':
                    if abs(int(a)-int(b)) == int(k):
                        return True
                return False
            

def grouping(): #this function matches the files depending on the name of each test.
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


if __name__ == '__main__':
    group_list = grouping() #group correctly the files.
    print("Hey! Type one of the following test names to see this test's solution!(if there is one)")
    for var_name, dom_name, ctr_name, test_name in group_list:
        print(test_name) #print all test names.
    go_on = 'Y'
    while go_on == 'Y':
        found = False
        name = input("Give me the test's name: ")
        for var_name, dom_name, ctr_name, test_name in group_list:
            if name == test_name: #if name given is the same with the test's name.
                found = True
                running_test = rlfa(var_name, dom_name, ctr_name) #create the object with class rlfa.
                result = backtracking_search(running_test, mrv, unordered_domain_values, forward_checking)
                print(result) #print the result of backtracking_search.
                go_on = input("\nWant to check more tests? Press Y for YES or anything else for NO: ")
        if found == False: #if name given doesn't belong to any test.
            print("Wrong input! Try again!")

            

