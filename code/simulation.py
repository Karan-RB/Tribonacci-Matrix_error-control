from tribonacci import Tribonacci
from error_inducing_functions import fix_errors
import numpy as np
import time
import matplotlib.pyplot as plt 


MAX_BITS_MSG = 8
rounds = [10000, 10000, 10000, 10000, 1000, 1000, 100, 100]
START = 8
END = 8

not_detected_errs = []
mis_corrected_errs = []
time_taken = []

for i in range(START, END+1):
    #create 2 tribonacci objects
    sender = Tribonacci(k=i)
    receiver = Tribonacci(k=i)

    #calculating the max number of bits in the encoded matrix
    max_num = max(sender.encode_matrix.flatten())
    max_bits_enc = int(np.ceil(np.log2(3*max_num))) + MAX_BITS_MSG

    #set the seed for np random
    np.random.seed(0)

    for j in range(1, 9):

        n_errors = j
        t_mis_corrected = 0
        t_not_detected = 0
        total_time = 0

        for _ in range(rounds[j-1]):

            #create a 3x3 matrix filled with integers and get its determinant
            msg = np.random.randint(0, 2**MAX_BITS_MSG-1, (3,3))

            start_enc = time.perf_counter()

            #send the message
            encoded, determinant = sender.send(msg)

            end_enc = time.perf_counter()
            
            #induce a single error in the encoded matrix
            fix_errors(encoded, num_errors=n_errors, n_bits=max_bits_enc)

            start_de = time.perf_counter()

            #receive the message and decode it
            corrected, decoded = receiver.receive(encoded, determinant)

            end_de = time.perf_counter()
            
            total_time += (end_enc - start_enc) + (end_de - start_de)

            if np.array_equal(msg, decoded):
                continue

            if not corrected:
                t_not_detected += 1

            else:
                t_mis_corrected += 1
        
        not_detected_errs.append(t_not_detected/rounds[j-1])
        mis_corrected_errs.append(t_mis_corrected/rounds[j-1])
        time_taken.append(total_time/rounds[j-1])
        
        print(f"For k = {i}:\nNot detected = {t_not_detected}\nMis_Corrected = {t_mis_corrected}\nTime={total_time/rounds[j]}\n")

#create a bar graph showing t_miscorrected over t_not_detected
fig = plt.subplots(figsize =(10, 10))
p1 = plt.bar(np.arange(1, 9), not_detected_errs)
p2 = plt.bar(np.arange(1, 9), mis_corrected_errs, bottom = not_detected_errs)
 
plt.ylabel('Incorrect count')
plt.xlabel('Number of folds of errors')
plt.title('Error correction failure frequency')
plt.xticks(np.arange(1, 9))
plt.legend((p1[0], p2[0]), ('Undetected_errors', 'Mis_corrected_errors'))
 
plt.savefig("correction_results.jpg")

#create a bar graph showing time taken for encoding and decoding
fig = plt.subplots(figsize =(10, 10))
p1 = plt.bar(np.arange(1, 9), time_taken)

plt.ylabel('Time taken (s)')
plt.xlabel('Number of folds of errors')
plt.title('Time taken for encoding and decoding')
plt.xticks(np.arange(1, 9))
