from  GaussianElimination import *

def GetLinearIndependentColumns (matrix) :
    mat = get_rows(get_columns(matrix))
    RREF = GetGaussianEliminationResult(matrix)
    zerorows = getZeroRows(RREF)
    rank = len(zerorows)
    LIcolumns = []
    for i in range(len(RREF)-len(zerorows)) :
        firstnonzeroindex = RREF[i].index(1)
        LIcolumns.append(get_columns(mat)[firstnonzeroindex])
    return LIcolumns

def rank(matrix) :
    return len(GetLinearIndependentColumns(matrix))

def isLinearlyIndependent(matrix) :
    return rank(matrix) == len(get_columns(matrix))

