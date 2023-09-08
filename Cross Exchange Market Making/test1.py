import time
from web3 import Web3

start_time = time.time()  # record the start time

while True:  # loop until break
    elapsed_time = time.time() - start_time  # calculate the elapsed time

    if elapsed_time <= 5:
        counter = 0
        while True:
            counter += 1
            elapsed_time = time.time() - start_time  # update elapsed_time
            if counter > 2000 or elapsed_time > 5:
                print(f'counter = {counter}')
                break

    elif elapsed_time > 5:
        print('more than 5 sec')
        break


