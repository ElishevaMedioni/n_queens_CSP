
import CSProblem
import copy


def solve(n):
    CSProblem.present(backtrack(CSProblem.create(n)))


def backtrack(p):
    var = next_var(p, MRV=True)  # MRV-Most constrained variable or Minimum Remaining Values
    if var == None:
        return p
    dom = sorted_domain(p, var, LCV=True)  # LCV-least constraining value
    for i in dom:
        bu = copy.deepcopy(p)
        CSProblem.assign_val(bu, var, i)
        propagate_constraints(bu, var)  #
        bu = backtrack(bu)
        if CSProblem.is_solved(bu):
            return bu
    return p


def sorted_domain(p, var, LCV=True):
    if LCV == False:
        return CSProblem.domain(p, var)
    else:
        list_number_of_del_place = []
        list_num_place = p[1][var]
        final_list = []
        for i in list_num_place:
            l = (p, var, i)
            # calling the function to know to num of val erased from the domains to each domain
            num = num_of_del_vals(l)
            list_number_of_del_place += [num]
        # pass through the list to find the minimum
        for j in range(0, len(list_number_of_del_place)):
            min = list_number_of_del_place[0]
            index = 0
            for k in range(0, len(list_number_of_del_place)):
                if min > list_number_of_del_place[k]:
                    min = list_number_of_del_place[k]
                    index = k
                    list_number_of_del_place[k] = 1000
            # create a final list with the domains sorted
            final_list += [list_num_place[index]]
            list_number_of_del_place.remove(list_number_of_del_place[index])
            list_num_place.remove(list_num_place[index])
        return final_list


def num_of_del_vals(l):
    # l=[problem, the variable, the val. assigned to the var.]
    # returns the num. of vals. erased from vars domains after assigning x to v
    count = 0
    for inf_v in CSProblem.list_of_influenced_vars(l[0], l[1]):
        for i in CSProblem.domain(l[0], inf_v):
            if not CSProblem.is_consistent(l[0], l[1], inf_v, l[2], i):
                count += 1
    return count


def next_var(p, MRV=True):
    # p is the problem
    # MRV - Minimum Remained Values
    # Returns next var. to assign
    # If MRV=True uses MRV heuristics
    # If MRV=False returns first non-assigned var.
    if MRV == False:
        v = CSProblem.get_list_of_free_vars(p)
        if v == []:
            return None
        else:
            return v[0]
    else:
        min = 1000
        index = 0
        for i in range(0, len(p[1])):
            # pass through the list of domains and check which one has the lowest values
            if min > len(p[1][i]) != 0:
                min = len(p[1][i])
                index = i
        return index


def propagate_constraints(p, v):
    for i in CSProblem.list_of_influenced_vars(p, v):
        for x in CSProblem.domain(p, i):
            if not CSProblem.is_consistent(p, i, v, x, CSProblem.get_val(p, v)):
                CSProblem.erase_from_domain(p, i, x)


solve(10)
