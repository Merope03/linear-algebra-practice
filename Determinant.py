from SolveEq import *

def checkUpptri(matrix) :
    for m in range(len(matrix)) :
        for n in range(len(matrix[0])) :
            if n<m and matrix[m][n] != 0 :
                return False
    return True            

def get_upptri_mat(matrix_origin) :
    matrix = get_rows(get_columns(matrix_origin))
    howmanychanged = 0
    pivot = find_pivot(matrix)
    print("\n주어진 행렬 : \n")
    showmatrix(matrix)
    if not pivot[0] == 0 :
        print("\n{0}행과 {1}행을 바꾼다.\n".format(0+1, pivot[0]+1))
        howmanychanged += 1
        matrix = Operation1(matrix, 0, pivot[0])
        showmatrix(matrix)
    for m in range(len(matrix)) :
        if (not m == 0) and not matrix[m][0] == 0 :
            print("\n{0}행에 {1}행의 {2}배를 더한다.\n".format(m+1, 0+1, -1*matrix[m][0]/matrix[0][0]))
            cont = -1*matrix[m][0]/matrix[0][0]
            matrix = Operation3(matrix, m, 0, cont)
            showmatrix(matrix)
    n = 1
    m = 1
    while not checkUpptri(matrix) :
        Semimatrix = get_rows(get_columns(matrix[m:])[n:])
        piv = find_pivot(Semimatrix)
        piv[0] = piv[0]+m
        piv[1] = piv[1]+n
        if not n == piv[0] :
            howmanychanged +=1
            matrix = Operation1(matrix, n, piv[0])
            showmatrix(matrix)
        for i in range(len(matrix)) :
            if (not(i == n)) and (not matrix[i][piv[1]] == 0) :
                cont = -1*matrix[i][piv[1]]/matrix[n][piv[1]]
                matrix = Operation3(matrix, i, n, cont)
                showmatrix(matrix)
        n = n+1
        m = m+1

    print("\n완료!\n")
    return matrix, howmanychanged

def det(matrix) :
    upptri, changed = silent_call(get_upptri_mat, matrix)
    determinant = 1
    for i in range(len(upptri)) :
        determinant *= upptri[i][i]
        if type(determinant) == float :
            determinant = round(determinant,4)
    if changed % 2 == 1 :
        determinant = determinant * (-1)
    if determinant == 0 :
        determinant = 0.00
    return determinant