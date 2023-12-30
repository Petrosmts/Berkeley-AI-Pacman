import os

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
                dom_list.remove((dom,cont2))
                break
        for ctr,cont3 in ctr_list:
            temp3 = "ctr" + temp
            if ctr == temp3:
                sol3 = cont3
                ctr_list.remove((ctr,cont3))
                break
        group_list.append((temp,sol1,sol2,sol3))
    return group_list

if __name__ == '__main__':
    grouping()
            

