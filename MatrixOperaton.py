from EigenValue import *
import math

def Prod(A,B) :
    # Matrix Multiplication A and 
    C = []
    for m in range(len(A)) :
        row = []
        for p in range(len(B[0])) :
            num = 0
            for k in range(len(A[0])) :
                num+=A[m][k]*B[k][p]
            row.append(num)
        C.append(row)
    return C


def scalarprod(matrix, c) :
    mat = copymatrix(matrix)
    for m in range(len(matrix)) :
        for n in range(len(matrix[0])) :
            mat[m][n]*= c
    return mat

def Add(A,B) :
    C = []
    for i in range(len(A)) :
        row = []
        for j in range(len(A[0])) :
            row.append(A[i][j]+B[i][j])
        C.append(row)
    return C

def normalize(vector : list) -> list :
    constant = 0
    for num in vector :
        constant+=num**2
    constant = math.sqrt(constant)
    for i in range(len(vector)) :
        vector[i] = vector[i]/constant
    return vector