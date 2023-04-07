import numpy as np
import itertools
from pyomo.environ import *
from pyomo.opt import SolverFactory
from model_helper_functions import *

"""
alpha =1.83928675521416
c2_3 = (alpha+1)/alpha
c1_3 = alpha
c1_2 = (alpha**2)/(alpha+1)"""

class Tribonacci:

    def __init__(self, k, n_bits=8):
        self.k = k
        self.n_bits = n_bits
        self._compute_matrices()
        self._compute_all_possible_error_combinations()
        self.model = get_base_model(self.e12min, self.e12max, self.e23min, self.e23max, self.e13min, self.e13max, self.n_bits, self.encode_matrix.max())
        self.solver = SolverFactory('couenne')
    
    def _compute_all_possible_error_combinations(self):

        self.combinations = []
        
        for i in range(8, 0, -1):
            self.combinations.extend([combination for combination in itertools.combinations(range(9), i)])
    
    def _compute_matrices(self):
        # Compute the encode and decode matrices
        k = self.k
        self.t = np.zeros((k + 4))
        if k < 4:
            raise ValueError("k must be at least 4")
        
        self.t[2] = 1
        for i in range(3, k + 4):
            self.t[i] = self.t[i - 1] + self.t[i - 2] + self.t[i - 3]
        
        self.encode_matrix = np.array([[self.t[k+i], self.t[k+i-1] + self.t[k+i-2], self.t[k+i-1]] for i in range(2, -1, -1)], dtype=np.int64)
        self.decode_matrix = np.linalg.inv(self.encode_matrix)

        self.e12min = min(self.t[k+i]/(self.t[k+i-1] + self.t[k+i-2]) for i in range(2, -1, -1))
        self.e12max = max(self.t[k+i]/(self.t[k+i-1] + self.t[k+i-2]) for i in range(2, -1, -1))

        self.e23min = min((self.t[k+i]+self.t[k+i-1])/self.t[k+i] for i in range(1, -2, -1))
        self.e23max = max((self.t[k+i]+self.t[k+i-1])/self.t[k+i] for i in range(1, -2, -1))

        self.e13min = min(self.t[k+i]/self.t[k+i-1] for i in range(2, -1, -1))
        self.e13max = max(self.t[k+i]/self.t[k+i-1] for i in range(2, -1, -1))


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
    
    def _check_rows(self, encoded_message):
        for row in encoded_message:
            e12 = row[0]/row[1]
            e23 = row[1]/row[2]
            e13 = row[0]/row[2]

            if e12 < self.e12min or e12 > self.e12max:
                return False
            if e23 < self.e23min or e23 > self.e23max:
                return False
            if e13 < self.e13min or e13 > self.e13max:
                return False
        
        return True
    
    def _check(self, encoded_message, determinant):
        #check if the determinant of the encoded message is equal to the determinant of the original message
        if int(np.round(np.linalg.det(encoded_message))) != determinant:
            return False

        if self._check_rows(encoded_message) == False:
            return False

        return True

    def receive(self, encoded_message, determinant):
        #print("Received encoded message: ", encoded_message, '\n')
        corrected = False
        
        if self._check(encoded_message, determinant) == False:

            corrected, recovered_msg = self.correct(encoded_message, determinant)

            if not corrected:
                return False, None
            
            encoded_message = recovered_msg
            
        return corrected, self.decode(encoded_message)-1
    
    def correct(self, encoded_message, determinant):
        
        instance = create_instance(self.model, determinant)
        values = encoded_message.flatten().tolist()
        
        for combination in self.combinations:

            problem = create_problem(instance, combination, values)
            solved = solve_problem(problem, self.solver)

            if not solved:
                continue

            recovered_msg = np.array([value(problem.a[i]) for i in range(9)], dtype=np.int64).reshape(3,3)
            return True, recovered_msg

        return False, None

    """
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
        
        return error"""
        

def test_single_error():
    trib = Tribonacci(10)
    print(trib.receive(np.array([[ 815,  684,  443], [2311, 1921, 1273], [3839, 3222, 2087]]), 0))

def test_double_error():
    trib = Tribonacci(10)
    print(trib.receive(np.array([[ 815,  684,  443], [2311, 1921, 1273], [1000, 3222, 2087]]), 0))       
    
