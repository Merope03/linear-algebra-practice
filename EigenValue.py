from InverseMatrix import *
from Determinant import *
from sympy import Symbol, solve, simplify, factor, re, im

lambda_symbol = Symbol('λ')
def copymatrix(matrix) :
    return get_rows(get_columns(matrix))

def ChaPoly(matrix) :
    mat = get_rows(get_columns(matrix))
    for n in range(len(mat)) :
        mat[n][n] -= lambda_symbol
    return factor(simplify(det(mat)))

def get_Eigen_vectors(matrix) :
    EigenDict = {}
    mat = copymatrix(matrix)
    cha_poly = ChaPoly(mat)
    eigenvalues = solve(cha_poly, lambda_symbol)
    real_eigenvalues = [float(re(num)) for num in eigenvalues if round(num,6).is_real]
    real_eigenvalues = [num for num in real_eigenvalues]
    for value in real_eigenvalues :
        A_lambdaI = copymatrix(mat)
        zero_vector = []
        for n in range(len(A_lambdaI)) :
            A_lambdaI[n][n] -= value
            zero_vector.append(0)
        Eigenspace = solve_linear_system(A_lambdaI, zero_vector)
        Eigenspace = Eigenspace[1:]
        EigenDict.update({round(value,2) : []})
        for eigenvector in Eigenspace :
            EigenDict[round(value,2)].append(eigenvector)
    return EigenDict

def Diagonalization(matrix) :
    Eigendict = get_Eigen_vectors(matrix)
    num_eigenvectors = 0
    for eigenvalue in Eigendict.keys() :
        num_eigenvectors += len(Eigendict[eigenvalue])
    D = []
    Q = []
    if num_eigenvectors!= len(matrix) :
        print('Cannot Diagonalize')
    else :
        n = 0
        for value in Eigendict.keys() :
            for vector in Eigendict[value] :
                D.append([value*(int(j==n)) for j in range(len(matrix)) ])
                Q.append(vector)
                n+=1
        Q = get_columns(Q)
        print('Q : ')
        showmatrix(Q)
        print('D : ')
        showmatrix(D)