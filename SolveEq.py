from LinearIndependent import *

def get_augmented(A,b) :
    columns = get_columns(A)
    columns.append(b)
    augmented = get_rows(columns)
    return augmented

def is_consistent(A, b) :# is Ax = b consistent?
    augmented = get_augmented(A,b)
    if rank(A) == rank(augmented) :
        return True
    else :
        return False
    
def solve_for_RREF(A,b) :
    if not (checkRREF(get_augmented(A,b)) and is_consistent(A,b)) :
        return
    solution = []
    pivot_elements_loc = []
    for m in range(len(A)) :
        if A[m] != [0 for num in A[m]] :
            pivot_elements_loc.append(A[m].index(1))
    nonpivot_column_loc = [num for num in range(len(get_columns(A))) if not(num in pivot_elements_loc)]
    for i in range(len(get_columns(A))-len(pivot_elements_loc)+1) :
        solelement = []
        if not (i== 0) :
            targetcolumn = nonpivot_column_loc[0]
            nonpivot_column_loc.remove(targetcolumn)
        for m in range(len(get_columns(A))) :
            if i == 0 :
                if m in pivot_elements_loc :
                    loc = pivot_elements_loc.index(m)
                    solelement.append(b[loc])
                else :
                    solelement.append(0)
            else :
                
                targetind = [ind for ye,ind in enumerate(pivot_elements_loc) if not (A[ye][targetcolumn] == 0)]
                
                if m == targetcolumn :
                    solelement.append(1)
                elif not (m in pivot_elements_loc) :
                    solelement.append(0)
                elif m in targetind :
                    temp = pivot_elements_loc.index(m)
                    solelement.append(-1*A[temp][targetcolumn])
                else :
                    solelement.append(0)


        solution.append(solelement)
    return solution

def solve_linear_system(A, b) :
    if not is_consistent(A,b) :
        print("No solution!")
        return []
    else :
        augmented = get_augmented(A,b)
        augmentedRREF = GetGaussianEliminationResult(augmented)
        A_rref = get_rows(get_columns(augmentedRREF)[:len(get_columns(augmentedRREF))-1])
        b_rref = get_columns(augmentedRREF)[-1]
        solved = solve_for_RREF(A_rref, b_rref)
        return solved