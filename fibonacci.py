def recursive(n):
    result = []
    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        result.append((recursive(n-1)+recursive(n-2)))
        return result

def iterative(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result
