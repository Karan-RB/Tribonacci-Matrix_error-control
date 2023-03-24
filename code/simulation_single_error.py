from time import sleep
from tribonacci import Tribonacci
from error_inducing_functions import induce_errors
import numpy as np
import matplotlib.pyplot as plt


MAX_BITS_MSG = 8
TOTAL_ROUNDS = 1000000
START = 2
END = 10

not_detected_errs = []
mis_corrected_errs = []

for i in range(START, END):
    #create 2 tribonacci objects
    sender = Tribonacci(k=i)
    receiver = Tribonacci(k=i)

    #calculating the max number of bits in the encoded matrix
    max_num = max(sender.encode_matrix.flatten())
    max_bits_enc = int(np.ceil(np.log2(3*max_num))) + MAX_BITS_MSG

    t_mis_corrected = 0
    t_not_detected = 0

    #set the seed for np random
    np.random.seed(0)

    for _ in range(TOTAL_ROUNDS):

        #create a 3x3 matrix filled with integers and get its determinant
        msg = np.random.randint(0, 2**MAX_BITS_MSG-1, (3,3))

        #send the message
        encoded, determinant = sender.send(msg)
        
        #induce a single error in the encoded matrix
        induce_errors(encoded, 1, max_bits_enc)

        #receive the message and decode it
        _, decoded, corrected = receiver.receive(encoded, determinant)

        if np.array_equal(msg, decoded):
            continue

        if not corrected:
            t_not_detected += 1

        else:
            #if det of encoded is -ve, then continue
            if np.linalg.det(encoded) < 0:
                continue
            print("Mis Corrected:")
            print("Message: ", msg)
            print("Encoded: ", sender.send(msg)[0])
            print("Encoded received: ", encoded)
            print("Encoded corrected:", sender.send(decoded)[0])
            print("determinant of encoded: ", np.linalg.det(encoded))
            print("Decoded: ", decoded)
            sleep(150)
            t_mis_corrected += 1
    
    not_detected_errs.append(t_not_detected)
    mis_corrected_errs.append(t_mis_corrected)
    
    print(f"For k = {i}:\nNot detected = {t_not_detected}\nMis_Corrected = {t_mis_corrected}\n")
    
#create a bar graph showing t_miscorrected over t_not_detected
fig = plt.subplots(figsize =(10, 10))
p1 = plt.bar(np.arange(START, END), not_detected_errs)
p2 = plt.bar(np.arange(START, END), mis_corrected_errs, bottom = not_detected_errs)
 
plt.ylabel('Incorrect count')
plt.xlabel('k')
plt.title('Single error correction failure counts')
plt.xticks(np.arange(START, END))
plt.legend((p1[0], p2[0]), ('Undetected_errors', 'Mis_corrected_errors'))
 
plt.savefig("single_error_results.jpg")
