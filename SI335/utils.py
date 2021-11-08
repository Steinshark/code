def smul(X, Y, B):
    n = len(X)
    A = [0 for x in range(2*n)]#zero-filled array of length (2*n)
    T = [0 for x in range(n)] #zero-filled array of length n
    for i in range(0, n):
        # set T = X * Y[i]
        carry = 0
        for j in range(0, n):
            carry, T[j] = divmod(X[j] * Y[i] + carry, B)
            print(carry)
        # add T to A, the running sum
        A[i : i+n+1] = add(A[i : i+n], T[0 : n], B)
        A[i+n] = A[i+n] + carry
    return A

def add(X, Y, B):
    n = len(X)
    carry = 0
    A = [0 for x in range(n+1)]
    for i in range(0, n):
        carry, A[i] = divmod(X[i] + Y[i] + carry, B)
    A[n] = carry
    return A

smul([9,8,7,6,5,4,3,2,1],[9,9,9],10)
