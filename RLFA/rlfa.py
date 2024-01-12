from csp import *


class rlfa(CSP):
    def __init__(self, variables, domains, constraints):
        self.ctrs_checked = 0 #how many constraints are checked.
        var_for_csp = [] #list with variables.
        dom_for_csp = {} #dictionary where the key is a variable and the element is a list with all possible values.
        neighs_for_csp = {} #dictionary where the key is a variable and the value is a list with all neighbors.
        dict_for_ctrs = {} #so we can know the symbol(> or =) for each constraint. This list will have tuples with each constraint properly seperated with function split(Tried list first but it was slow due to O(n).
        weights_for_ctrs = {} #dictionary where the key is each constraint.
        dict_of_conflicts = {}
        for index, var in enumerate(variables):
            if index > 0: #first element is the amount of variables, we don't want to check that.
                var_domain = var.split(" ") #variable is var_dom[0], domain is var_dom[1].
                var_for_csp.append(var_domain[0]) #put variable in list for the csp.__init__.
                neighs_for_var = [] #list with neighbors of each variable
                dict_of_conflicts[var_domain[0]] = []
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
                        key = (tctr[0], tctr[1]) 
                        rev_key = (tctr[1], tctr[0])
                        value = (tctr[2], tctr[3])
                        dict_for_ctrs[key] = value
                        weights_for_ctrs[key] = 1 #weight of each constraint is initialized with 1.
                        weights_for_ctrs[rev_key] = 1 #we initialize a weight for the reversed constraint too. 
                        if var_domain[0] == tctr[0]: #if the variable we are examining is the first variable in each constraint, then the second is neighbor of the first.
                            neighs_for_var.append(tctr[1])
                        elif var_domain[0] == tctr[1]: #if the variable we are examining is the second variable in each constraint, then the first is neighbor of the second.
                            neighs_for_var.append(tctr[0])
                neighs_for_csp[var_domain[0]] = neighs_for_var
                self.dict_for_ctrs = dict_for_ctrs
                self.weights_for_ctrs = weights_for_ctrs
                self.dict_of_conflicts = dict_of_conflicts
            super().__init__(var_for_csp, dom_for_csp, neighs_for_csp, self.f) #calling the CSP class init function with super().__init__ giving the necessary arguments.


    def f(self, A, a, B, b): #constraint function 
        symbol, k = self.dict_for_ctrs.get((A, B)) or self.dict_for_ctrs.get((B, A)) #variables might be given with the wrong order.
        self.ctrs_checked += 1 #increase how many constraints are checked.
        if symbol == '>':
            return abs(int(a)-int(b)) > int(k)
        elif symbol == '=':
            return abs(int(a)-int(b)) == int(k)
        return False
            
def var_weight(assignment, var, csp): #for dom_wdeg
    total_sum = 1
    for neigh in csp.neighbors[var]:
        if neigh in assignment: #Hence, the weighted degree of a variable Xi corresponds to the sum of the weights of the constraints involving Xi and at least another uninstantiated variable(from file given in hw3-2023.pdf for dom_wdeg).
            continue
        key = (var, neigh)
        total_sum += csp.weights_for_ctrs[key] #sum all weights that have (var, a neighbor of var) for key.
    return total_sum

def dom_wdeg(assignment, csp):
    csp.support_pruning()
    minimum = float('inf')
    for var in csp.variables:
        if var not in assignment: #we don't want var to have a value.
            dom = len(csp.curr_domains[var]) #length of current domain with inconsistent values removed.
            wdeg = var_weight(assignment, var, csp) #sum all weights from constraints that have var in them.
            ratio = dom / wdeg 
            if ratio < minimum: #we are searching for the variable that has the lowest dom / wdeg.
                variable_returned = var
                minimum = ratio
    return variable_returned #we return the value with the lowest dom / wdeg value.


def fc_with_dom_wdeg(csp, var, value, assignment, removals): #same with the fc algorithm in csp file but we increase weights where it is needed.
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b): #if a variable B causes deletion of a value for variable var, then B must be put in conflicts of var.
                    if var not in csp.dict_of_conflicts[B]:
                        csp.dict_of_conflicts[B].append(var)
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]: #if there is not a value that satisfies the constraint, we increase the weight in two ways.
                key = (var, B)
                rev_key = (B, var)
                csp.weights_for_ctrs[key] += 1 #first way
                csp.weights_for_ctrs[rev_key] += 1 #second way
                return False
    return True


def AC3_with_dom_wdeg(csp, queue=None, removals=None, arc_heuristic=dom_j_up): #same with the AC-3 algorithm in csp file but we increase weights where it is needed.
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]: #if there is not a value that satisfies the constraint, we increase the weight in two ways.
                key = (Xi, Xj)
                rev_key = (Xj, Xi)
                csp.weights_for_ctrs[key] += 1 #first way
                csp.weights_for_ctrs[rev_key] += 1 #second way
                return False, checks # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks # CSP is satisfiable


def mac_with_dom_wdeg(csp, var, value, assignment, removals, constraint_propagation=AC3_with_dom_wdeg):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def delete_from_conflicts(csp, var):
    for con in csp.dict_of_conflicts: #check in all variables' conflicts.
            if var in csp.dict_of_conflicts[con]:
                csp.dict_of_conflicts[con].remove(var)

def transfer_of_conflicts(csp, var, deepest_var):
    for con in csp.dict_of_conflicts[var]: #transfer conflicts of variable var to conflicts to conflicts of variable deepest_var.
            if con != deepest_var and con not in csp.dict_of_conflicts[deepest_var]:
                    csp.dict_of_conflicts[deepest_var].append(con)

found = False
def fc_cbj(csp, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values, inference=no_inference):
    #names of variables are similar to those in function backtracking search.  
    def backjump(assignment):
        global found #so I can print the result either None, because my code doesn't return the assignment.
        found = False
        if len(assignment) == len(csp.variables): #if the assignment has all variables in it, then we found solution!
            found = True
            print(assignment,"\n")
            return None
        var = select_unassigned_variable(assignment, csp) #from line 148 to line 154, code is similar to function backtrack in backtracking_search in csp.py.
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backjump(assignment)
                    if var != result: #if the result isn't what we want, we continue backjumping after we unassign the variable, delete var from all dict_of_conflicts and restore the removed values.
                        csp.unassign(var, assignment)
                        delete_from_conflicts(csp, var)
                        csp.restore(removals)
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment) #if all values are checked, then we unassign.
        delete_from_conflicts(csp, var) #we delete var from all dict_of_conflicts
        if len(csp.dict_of_conflicts[var]) > 0:
            deepest_var = csp.dict_of_conflicts[var][len(csp.dict_of_conflicts[var]) - 1] #put all variables from conflicts of var to conflicts of deepest_var so we don't lose information about conflicts.
            transfer_of_conflicts(csp, var, deepest_var)
            return deepest_var 

    result = backjump({})
    if found == False:
        print(None, "\n")
    return result

