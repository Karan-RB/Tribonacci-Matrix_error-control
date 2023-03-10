import numpy as np
from sympy.solvers.diophantine import diop_solve
from sympy.abc import x, y, t

alpha =1.83928675521416
c2_3 = (alpha+1)/alpha
c1_3 = alpha
c1_2 = (alpha**2)/(alpha+1)

class Tribonacci:

    def __init__(self, k, n_bits=8):
        self.k = k
        self.n_bits = n_bits
        self._compute_matrices()
    
    def _compute_matrices(self):
        # Compute the encode and decode matrices
        k = self.k
        t = np.zeros((k + 3))
        if k < 2:
            raise ValueError("k must be at least 2")
        
        t[2] = 1
        for i in range(3, k + 3):
            t[i] = t[i - 1] + t[i - 2] + t[i - 3]
        
        self.encode_matrix = np.array([[t[k+i], t[k+i-1] + t[k+i-2], t[k+i-1]] for i in range(2, -1, -1)], dtype=np.int64)
        self.decode_matrix = np.linalg.inv(self.encode_matrix)

    def encode(self, message):
        #multiply message matrix with encode matrix
        return np.matmul(message, self.encode_matrix)
    
    def decode(self, encoded_matrix):
        #multiply encoded matrix with decode matrix
        float_decoded = np.matmul(encoded_matrix, self.decode_matrix)
        return np.round(float_decoded).astype(int)
    
    def send(self, message):
        #add 1 to each element of the matrix to avoid 0s in the encoded matrix
        return self.encode(message+1), int(np.round(np.linalg.det(message+1)))

    #we are going to use xor to mutate the message after generating a number where p(any bit = 1) = error_rate
    def _mutate(self, message, error_rate=0.01):
            
        def get_num():
            seq = np.random.choice(["0", "1"], size=self.n_bits, p=[1-error_rate, error_rate])
            return int("".join(seq), 2)
        
        for i in range(len(message)):
            for j in range(len(message[0])):
                message[i][j] ^= get_num()
        
        return message
    
    def _check(self, encoded_message, determinant):
        #check if the determinant of the encoded message is equal to the determinant of the original message
        if int(np.round(np.linalg.det(encoded_message))) == determinant:
            return True
        return False

    def receive(self, encoded_message, determinant):
        #print("Received encoded message: ", encoded_message, '\n')
        corrected = False
        
        if self._check(encoded_message, determinant) == False:
            corrected = True
            self.correct(encoded_message, determinant)
            
        return encoded_message, self.decode(encoded_message)-1, corrected
    
    def correct(self, msg, determinant):

        #correct single errors
        done = self._correct_single(msg, determinant)
        if done:
            return True
        
        #correct double errors
        """done = self._correct_double(msg, determinant)
        if done:
            return True"""

        return False

    def _correct_single(self, msg, determinant):
        cofactors = np.zeros((3,3), dtype=np.int64) #minors_det[i] = det of minor of msg with element corresponding to x_i+1 removed

        for i in range(3):
            for j in range(3):
                cofactors[i][j] = (-1)**(i+j)*int(np.round(np.linalg.det(np.delete(np.delete(msg, i, 0), j, 1))))

        pcv = np.zeros((3,3)) #possible corrected values

        possible_corrections = []

        for i in range(3):
            for j in range(3):
                
                if cofactors[i][j] == 0:
                    continue

                pcv[i][j] = (determinant - msg[i][1 if j == 0 else 0]*cofactors[i][1 if j == 0 else 0] - msg[i][1 if j == 2 else 2]*cofactors[i][1 if j == 2 else 2])/cofactors[i][j]
                
                if pcv[i][j].is_integer():
                    possible_corrections.append((i, j, int(pcv[i][j])))
        
        if len(possible_corrections) == 0:
            return False
        
        best_fit = self._best_fit_single_error(msg, determinant, possible_corrections)
        msg[best_fit[0]][best_fit[1]] = best_fit[2]


    def _form_dio_eq(self, msg, determinant, positions_variables):
        m = msg
        pass

    def _correct_double(self, msg, determinant):

        pass
    
    def _best_fit_single_error(self, msg, determinant, possible_corrections):
        #find the best fit correction
        best_fit = None
        best_fit_error = float('inf')

        for i, j, val in possible_corrections:
            error = self._satisfies(msg, determinant, i, j, val)
            
            if error == -1:
                continue

            if error < best_fit_error:
                best_fit_error = error
                best_fit = (i, j, val)
        
        return best_fit

    def _satisfies(self, msg, determinant, i, j, val):
        tmp = msg[i][j]
        msg[i][j] = val

        if int(np.round(np.linalg.det(msg))) != determinant:
            msg[i][j] = tmp
            return -1
        
        c1 = msg[i][0]
        c2 = msg[i][1]
        c3 = msg[i][2]
        msg[i][j] = tmp

        if c1 == 0 or c2 == 0 or c3 == 0:
            return float('infinity')
        
        error = (abs(c1/c3 - c1_3) + abs(c2/c3 - c2_3) + abs(c1/c2 - c1_2))
        
        return error
        

def test_single_error():
    trib = Tribonacci(10)
    print(trib.receive(np.array([[ 815,  684,  443], [2311, 1921, 1273], [3839, 3222, 2087]]), 0))

def test_double_error():
    trib = Tribonacci(10)
    print(trib.receive(np.array([[ 815,  684,  443], [2311, 1921, 1273], [1000, 3222, 2087]]), 0))       
    


