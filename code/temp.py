import numpy as np

def compute(k = 10):
    t = np.zeros((k + 4))
    if k < 2:
        raise ValueError("k must be at least 2")
    
    t[2] = 1
    for i in range(3, k + 4):
        t[i] = t[i - 1] + t[i - 2] + t[i - 3]
    
    encode_matrix = np.array([[t[k+i], t[k+i-1] + t[k+i-2], t[k+i-1]] for i in range(2, -1, -1)], dtype=np.int64)
    decode_matrix = np.linalg.inv(encode_matrix)

    e12min = min(t[k+i]/(t[k+i-1] + t[k+i-2]) for i in range(2, -1, -1))
    e12max = max(t[k+i]/(t[k+i-1] + t[k+i-2]) for i in range(2, -1, -1))

    e23min = min((t[k+i]+t[k+i-1])/t[k+i] for i in range(1, -2, -1))
    e23max = max((t[k+i]+t[k+i-1])/t[k+i] for i in range(1, -2, -1))

    e13min = min(t[k+i]/t[k+i-1] for i in range(2, -1, -1))
    e13max = max(t[k+i]/t[k+i-1] for i in range(2, -1, -1))

    print(e12min, e12max, sep="\t")
    print(e23min, e23max, sep="\t")
    print(e13min, e13max, sep="\t")

    #generate a 3x3 matrix of positive 8 bit integers
    message = np.random.randint(0, 2**8, size=(3, 3))
    print(message)
    #print its determinant
    print(np.linalg.det(message))
    mat2 = np.matmul(message, encode_matrix)   
    print(mat2) 
    print(np.linalg.det(mat2))
    return list(np.matmul(message,encode_matrix).flatten())


print(compute(10))


