import time
from itertools import permutations
import sys
import matplotlib.pyplot as plt
import numpy as np


def calcRedundantBits(m):
    # Use the formula 2 ^ r >= m + r + 1
    # to calculate the no of redundant bits.
    # Iterate over 0 .. m and return the value
    # that satisfies the equation

    for i in range(m):
        if (2 ** i >= m + i + 1):
            return i


def posRedundantBits(data, r):
    # Redundancy bits are placed at the positions
    # which correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''

    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m + r + 1):
        if (i == 2 ** j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1

    # The result is reversed since positions are
    # counted backwards. (m + r+1 ... 1)
    return res[::-1]


def calcParityBits(arr, r):
    n = len(arr)

    # For finding rth parity bit, iterate over
    # 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):

            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])
            # -1 * j is given since array is reversed

        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
    return arr


def detectError(arr, nr):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])

        # Create a binary no by appending
        # parity bits together.

        res = res + val * (10 ** i)

    # Convert binary to decimal
    return int(str(res), 2)


def permutate(text):
    permutationList = permutations(text)
    permutationList = [''.join(tuples) for tuples in permutationList]

    # print(permutationList)
    # print("size in bytes: " + str(
    #     sys.getsizeof(permutationList)))  # This function returns the size of the object in bytes
    # print("size in bits: " + str(sys.getsizeof(permutationList) * 8))

    return permutationList


def evenParity(binaryString):
    counter = 0
    for bit in binaryString:
        if bit == '1':
            counter = counter + 1
    if counter % 2 == 1:
        result = binaryString + "1"
    else:
        result = binaryString + "0"
    return result

def oddParity(binaryString):
    counter = 0
    for bit in binaryString:
        if bit == '1':
            counter = counter + 1
    if counter % 2 == 0:
        result = binaryString + "1"
    else:
        result = binaryString + "0"
    return result


if __name__ == '__main__':

    permutationStringsList = ["ab", "abc", "abcd"]

    iterations = 200

    # Creating Timer
    startTime = time.perf_counter()
    endTime = time.perf_counter()

    parityTimeNsList = []
    hammingTimeNsList = []
    parityTimeNsSum = 0
    hammingTimeNsSum = 0

    for permutationString in permutationStringsList:

        permutationList = permutate(permutationString)
        binaryStringList = []

        for permutation in permutationList:
            for char in permutation:
                # Converting String to binary
                binaryString = ''.join(format(char, '08b') for char in bytearray(permutation, encoding='ascii'))
            binaryStringList.append(binaryString)

        # print(permutationList)
        print("The String \'" + permutationString + "\' is being permutated ...")
        print("Size in bytes: " + str(
            sys.getsizeof(permutationList)))  # This function returns the size of the object in bytes
        print("Size in bits: " + str(sys.getsizeof(permutationList) * 8))
        print("Number of permutations: " + str(len(permutationList)))

        for i in range(1, iterations):

            # Starting Counter
            startTime = time.perf_counter_ns()

            for x in binaryStringList:
                evenParity(x)

            endTime = time.perf_counter_ns()
            timeNs = endTime - startTime
            parityTimeNsSum = parityTimeNsSum + timeNs

        parityTimeNsList.append(parityTimeNsSum / iterations)
        parityTimeNsSum = 0

        for i in range(1, iterations):

            startTime = time.perf_counter_ns()

            # starting hamming
            for data in binaryStringList:
                # Calculate the no of Redundant Bits Required
                m = len(data)
                r = calcRedundantBits(m)

                # Determine the positions of Redundant Bits
                arr = posRedundantBits(data, r)

                # Determine the parity bits
                arr = calcParityBits(arr, r)

                # Data to be transferred
                # print("Data transferred is " + arr)

                # Stimulate error in transmission by changing
                # a bit value.
                # 10101001110 -> 11101001110, error in 10th position.
                arr = arr  # introduction of error
                # print("Error Data is " + arr)
                correction = detectError(arr, r)
                if (correction == 0):
                    # print("There is no error in the received message.")
                    continue
                else:
                    # print("The position of error is ", len(arr) - correction + 1, "from the left")
                    break

            endTime = time.perf_counter_ns()
            timeNs = endTime - startTime
            hammingTimeNsSum = hammingTimeNsSum + timeNs

        hammingTimeNsList.append(hammingTimeNsSum / iterations)
        hammingTimeNsSum = 0

    print(parityTimeNsList)
    print(hammingTimeNsList)


    # Plot
    wordsize = []
    for i in permutationStringsList:
        wordsize.append(len(i))

    legend_labels = ['Parity Check', 'Hamming Code']
    data1 = parityTimeNsList
    data2 = hammingTimeNsList
    width = 0.25
    position = np.arange(len(wordsize))

    # plt.bar(position, data1, width)
    # plt.bar(position + width, data2, width)
    # plt.xticks(position, wordsize)
    # plt.xlabel("Länge der permutierten Strings", fontsize=14)
    # plt.ylabel("Berechnungsdauer (in Nanosekunden)", fontsize=14)
    # plt.title("Durchschnittliche Berechnungsdauer\n der ECCs nach " + str(iterations) + " Wiederholungen", fontsize=15)
    # plt.legend(legend_labels, loc=1)


    # plt.bar(position, data1)
    plt.bar(position, data2, color="orange")
    plt.xticks(position, wordsize)
    plt.xlabel("Länge der permutierten Strings", fontsize=16)
    plt.ylabel("Berechnungsdauer (in Nanosekunden)", fontsize=16)
    plt.title("Durchschnittliche Berechnungsdauer \nnach " + str(iterations) + " Wiederholungen", fontsize=16)
    plt.show()


