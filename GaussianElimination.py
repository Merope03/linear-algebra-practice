import contextlib
import io

def silent_call(func, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)

def showmatrix(matrix) :
    for n in range(len(matrix)) :
        for m in range(len(matrix[0])) :
            if type(matrix[n][m]) in [float, int] :
                matrix[n][m] = float(matrix[n][m])
                if matrix[n][m] == 0 :
                    print('{0:>7.2f}'.format(0.00),end = ' ')
                else : 
                    print('{0:>7.2f}'.format(matrix[n][m]),end = ' ')
            else :
                print('{:>7}'.format(str(matrix[n][m])), end = ' ')
        print(end = '\n')

def get_columns(matrix) :
    colmat = []
    for n in range(len(matrix[0])) :
        colmatcomp = []
        for m in range(len(matrix)) :
            colmatcomp.append(matrix[m][n])
        colmat.append(colmatcomp)
    return colmat

def get_rows(colmat) :
    mat = []
    for m in range(len(colmat[0])) : 
        matcomp = []
        for n in range(len(colmat)) :
            matcomp.append(colmat[n][m])
        mat.append(matcomp)
    return mat


def Operation1(matrix_origin, r, s) :
    matrix = matrix_origin
    # change r low and s low
    a = matrix[r]
    matrix[r] = matrix[s]
    matrix[s] = a
    return matrix

def Operation2(matrix_origin, r, k) :
    # scalar multiplication k for r low
    matrix = matrix_origin
    matrix[r] = [k*num for num in matrix[r]]
    return matrix

def Operation3(matrix_origin, r, s, k) :
    # add multiplication k of s to r
    matrix = matrix_origin
    mult = [k*num for num in matrix[s]]
    for i in range(len(matrix[0])) :
        matrix[r][i] = mult[i]+matrix[r][i]
    return matrix

def find_pivot(matrix) :
    # 가장 왼쪽에 있는 0이 아닌 아이를 찾는다
    columns = get_columns(matrix)
    isFindNonzero = False
    index = [0,0]
    n = 0
    while isFindNonzero == False :
        if not columns[n] == [0 for num in columns[n]] :
            isFindNonzero = True
            index[1] = n
            index[0] = [num == 0 for num in columns[n]].index(False)
        n = n + 1   
    return index

def getZeroRows(matrix) :
    ZeroRows = []
    for m in range(len(matrix)) :
        if matrix[m] == [0 for i in matrix[m]] :
            ZeroRows.append(m)
    return ZeroRows

def CheckFirstConditionRREF(matrix) :
    zerorows = getZeroRows(matrix)
    if not zerorows == [] :
        for i in range(1, len(zerorows)+1) :
            if not (len(matrix) - i in zerorows) :
                return False
    return True

def CheckSecondConditionRREF(matrix) :
    columns = get_columns(matrix)
    for m in range(len(matrix)) :
        if not matrix[m] == [0 for num in matrix[m]] :
            piv = [num == 0 for num in matrix[m]].index(False)
            if not ([n == 0 for n in columns[piv]].count(False) == 1) :
                return False
    return True

def CheckThirdConditionRREF(matrix) : 
    for m in range(len(matrix)) :
        if not matrix[m] == [0 for num in matrix[m]] :
            piv = [num == 0 for num in matrix[m]].index(False)
            if not matrix[m][piv] == 1  :
                return False
    for m in range(1, len(matrix)) :
        if (not matrix[m] == [0 for num in matrix[m]]) and (not matrix[m-1] == [0 for num in matrix[m-1]]) :
            firstpivot = [num == 0 for num in matrix[m-1]].index(False)
            secondpivot = [num == 0 for num in matrix[m]].index(False)
            if firstpivot >= secondpivot : 
                return False
    return True

def checkRREF(matrix) :
    return CheckFirstConditionRREF(matrix) and CheckSecondConditionRREF(matrix) and CheckThirdConditionRREF(matrix)

def SortZeroRows(matrix_origin) :
    matrix = matrix_origin
    zerorows = getZeroRows(matrix)
    if not (zerorows == []) and not CheckFirstConditionRREF(matrix) :
        modifiedmat = []
        for m in range(len(matrix)) :
            if not(m in zerorows) :
                modifiedmat.append(matrix[m])
        for i in range(len(zerorows)) :
            modifiedmat.append([0 for nums in  matrix[0]])
        matrix = modifiedmat
    return matrix

def GaussianElimination(matrix_origin) :
    matrix = get_rows(get_columns(matrix_origin))
    UsedOperation = []
    pivot = find_pivot(matrix)
    print("\n주어진 행렬 : \n")
    n = 0
    m = 0
    while not checkRREF(matrix) :
        Semimatrix = get_rows(get_columns(matrix[m:])[n:])
        piv = find_pivot(Semimatrix)
        piv[0] = piv[0]+m
        piv[1] = piv[1]+n
        if not n == piv[0] :
            print("\n {0}행과 {1}행을 바꾼다.\n".format(n+1, piv[0]+1))
            UsedOperation.append("A,"+str(n+1)+","+str(piv[0]+1))
            matrix = Operation1(matrix, n, piv[0])
            showmatrix(matrix)
        if not matrix[n][piv[1]] == 1 :
            print("\n {0}행을 정규화한다.\n".format(n+1))
            UsedOperation.append("B,"+str(n+1)+","+str(1/(matrix[n][piv[1]])))
            matrix = Operation2(matrix, n, 1/(matrix[n][piv[1]]))
            showmatrix(matrix)
        for i in range(len(matrix)) :
            if (not(i == n)) and (not matrix[i][piv[1]] == 0) :
                cont = -1*matrix[i][piv[1]]
                UsedOperation.append("C,"+str(i+1)+","+str(n+1)+","+str(cont))
                print("\n{0}행에 {1}행의 {2:.2f}배를 곱해서 더한다.\n".format(i+1, n+1, -1*matrix[i][piv[1]]))
                matrix = Operation3(matrix, i, n, -1*matrix[i][piv[1]])
                showmatrix(matrix)
        matrix = CleanMatrix(matrix, 8)
        n = n+1
        m = m+1
    matrix = CleanMatrix(matrix, 2)
    print("\n완료!\n")
    
    L = []
    L.append(matrix)
    L.append(UsedOperation)
    return L

def CleanMatrix(matrix_origin, digit) :
    matrix = get_rows(get_columns(matrix_origin))
    for m in range(len(matrix)) :
        for n in range(len(matrix[0])) :
            if type(matrix[m][n]) == float :
                matrix[m][n] = round(matrix[m][n], digit)
            if abs(matrix[m][n] -0) < 0.01  :
                    matrix[m][n] = 0.00
    return matrix

def GaussianEliminationResult(matrix) :
        return (silent_call(GaussianElimination, matrix))

    
def GetGaussianEliminationResult(matrix) :
    return GaussianEliminationResult(matrix)[0]

def GetGaussianEliminationProcess(matrix) :
    return GaussianEliminationResult(matrix)[1]


