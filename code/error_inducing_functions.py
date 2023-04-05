# Description: This file contains functions that induce errors in the encoded matrix (3x3)
import random
import numpy as np

def fix_errors(message, num_errors=1, n_bits=8):

    # Choose random positions to induce errors
    error_positions = random.sample(range(9), num_errors)

    # Induce errors
    for pos in error_positions:
        num = np.random.randint(0, 2**n_bits-1)
        message[pos//3][pos%3] = num if num != message[pos//3][pos%3] else num+1

    return message

#we are going to use xor to mutate the message after generating a number where p(any bit = 1) = error_rate
def induce_errors(message, error_rate=0.01, n_bits=8):
        
    def get_num():
        seq = np.random.choice(["0", "1"], size=n_bits, p=[1-error_rate, error_rate])
        return int("".join(seq), 2)
    
    for i in range(len(message)):
        for j in range(len(message[0])):
            message[i][j] ^= get_num()
    
    return message