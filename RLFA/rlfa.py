import os
from csp import *

class rlfa(CSP):
    def __init__(self, variables, domains, neighbors, constraints):
        var_for_csp = [] #list with variables.
        dom_for_csp = {} #dictionary where the key is a variable and the element is a list with all possible values.
        neighs_for_csp = {}
        global dict_for_con_function 
        for index, var in enumerate(variables):
            if index > 0:
                var_domain = var.split(' ') #variable is var_dom[0], domain is var_dom[1].
                var_for_csp.append(var_domain[0]) #put variable in list for the csp.__init__.
                neighs_for_var = []
                for ind_ex, dom in enumerate(domains):
                    if ind_ex > 0:
                        if dom[0] == var_domain[1][0]: #if the variable's domain is the one we are examining.
                            tdom = dom.split(' ')
                            domain_size = tdom[1]
                            last_size = len(tdom[domain_size - 1])
                            tdom[domain_size - 1] = tdom[domain_size - 1][0 : last_size - 1] #last element must not have \n in it.
                            dom_values = [tdom[i] for i in range(2, domain_size)]
                            dom_for_csp[var_domain[0]] = dom_values
                for in_dex, ctr in enumerate(constraints):
                    if in_dex > 0:
                        tctr = ctr.split(' ')
                        last_size = len(tctr[len(tctr) - 1])
                        tctr[len(tctr) - 1] = tctr[len(tctr) - 1][0 : last_size - 1]
                        if var_domain[0] == tctr[0]:
                            neighs_for_var.append(tctr[1])
                        elif var_domain[0] == tctr[1]:
                            neighs_for_var.append(tctr[0])
                neighs_for_csp[var_domain[0]] = neighs_for_var
        CSP.__init__(self, var_for_csp, dom_for_csp, neighs_for_csp, f)


def f(A, a, B, b):
    

def grouping():
    content = list()
    var_list = list()
    dom_list = list()
    ctr_list = list()
    dir = '/home/petrakis/ArtIn/RLFA/rlfap'
    if os.path.exists(dir) == True: 
        for name in os.listdir(dir) : 
            if name != "odigies.txt" and name[len(name) - 4 : len(name)] == ".txt": 
                with open(os.path.join(dir,name)) as cur_file: 
                    content = cur_file.readlines()
                    if name[0] == 'v':
                        var_list.append((name, content))
                    elif name[0] == 'd':
                        dom_list.append((name, content))
                    elif name[0] == 'c':
                        ctr_list.append((name, content))
                    cur_file.close()
    else: 
        print("Error: Directory given is wrong!")
    group_list = list()
    temp = list()
    for var,cont1 in var_list:
        sol1 = cont1
        temp = var[3:len(var)]
        for dom,cont2 in dom_list:
            temp2 = "dom" + temp
            if dom == temp2:
                sol2 = cont2
                dom_list.remove((dom, cont2))
                break
        for ctr,cont3 in ctr_list:
            temp3 = "ctr" + temp
            if ctr == temp3:
                sol3 = cont3
                ctr_list.remove((ctr, cont3))
                break
        group_list.append((sol1, sol2, sol3, temp))
    return group_list

if __name__ == '__main__':
    grouping()
            

