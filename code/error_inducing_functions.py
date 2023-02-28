# Description: This file contains functions that induce errors in the encoded matrix (3x3)
import random
import numpy as np

def induce_errors(message, num_errors=1, n_bits=8):

    # Choose random positions to induce errors
    error_positions = random.sample(range(9), num_errors)

    # Induce errors
    for pos in error_positions:
        num = np.random.randint(0, 2**n_bits-1)
        message[pos//3][pos%3] = num if num != message[pos//3][pos%3] else num+1

    return message