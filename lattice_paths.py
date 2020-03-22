

import math
from itertools import combinations
from itertools import permutations
from datetime import datetime

#from sql_fns import store_dwell_times


def binomial_coefficient(n, k):
    if k == 0 or n == 0:
        return 1
    if k > n:
        return 0
    if n > 40:
        if n == k:
            return 0
        #value = stirling(n) / (stirling(k) * stirling(n-k))
        #print(value)
        #value = stirling_ln(n) / (stirling_ln(k) * stirling_ln(n-k))
        x = stirling_ln(n) - (stirling_ln(k) + stirling_ln(n-k))
        if x > 5:
            #value2 = 1 + x + x**2/2 + x**3/6 + x**4/24 + x**5/120 + x**6/720
            value2 = math.e**x
        else:
            value2 = math.e**x
        #print(value2)
        return value2
    else:
        value = math.factorial(n) / (math.factorial(k) * math.factorial(n-k))
        return value


def number_bound_paths(a,b,c,d):
    bn1 = c + d - a - b
    bd1  = c - a
    bn2 = c + d - a - b
    bd2 = c - b + 1
    #print('coefficients', bn1, bd1, bn2, bd2)

    all_path_count = binomial_coefficient(bn1, bd1)
    invalid_path_count = binomial_coefficient(bn2, bd2)
    valid_path_count = all_path_count - invalid_path_count
    #print('valid_path_count:', valid_path_count)
    return valid_path_count


def stirling(n):
    value = math.sqrt(2 * math.pi * n) * (n / math.e)**n
    return value


def stirling_ln(n):
    #value = math.sqrt(2 * math.pi * n) * (n / math.e)**n
    value = 0.5 * math.log(2 * math.pi * n) + n * math.log(n) - n
    #return math.e**value
    return value


def valid_paths():
    m = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]#,23,24,25,26]
    print(len(m)/2)

    M = len(m) + 2
    # max of 1's entered should reduce a bit
    # once the known number is hit, that should also reduce a bit
    t0 = datetime.now()
    valid_paths_list = []
    full_dwell = 0
    for item in combinations(m,int(len(m)/2)):
        l0 = [1] + [-1] * (len(m) + 1)
        for element in item:
            l0[element] = 1
        n = 0
        valid = 1
        for element in l0:
            n += element
            if n < 0:
                valid = 0
                break
            if n == len(m)/2:
                break
        if valid == 1:


            valid_paths_list.append(l0)
    #for path in valid_paths_list:
        #dwell_list = [item[0] * item[1] for item in zip(path, [0] + m + [m[-1] + 1])]
        #print(dwell_list)

        #dwell = -1 * sum([item[0] * item[1] for item in zip(path, [0] + m + [m[-1] + 1])])
            dwell = -1 * sum([item[0] * item[1] for item in zip(l0, [0] + m + [m[-1] + 1])])
            full_dwell += dwell
            #print(dwell, l0)
        #print(dwell, len(path))
            #store_dwell_times(M, [dwell])

    print(len(valid_paths_list))
    print(full_dwell/len(valid_paths_list))
    print(datetime.now() - t0)


if __name__ == '__main__':
    valid_paths()
    #number_bound_paths(0,0,4,4)
    # print('---')
    # a = number_bound_paths(1,0,3,3)
    # b = number_bound_paths(0,0,1,0)
    # print(a * b)
    # print('---')
    # print('---')
    # a = number_bound_paths(2,0,3,3)
    # b = number_bound_paths(0,0,2,0)
    # print(a * b)
    # c = number_bound_paths(1,1,3,3)
    # d = number_bound_paths(0,0,1,1)
    # print(c * d)
    # print(a * b + c * d)
    # print('---')
    # print('---')
    # a = number_bound_paths(3,0,3,3)
    # b = number_bound_paths(0,0,3,0)
    # print(a * b)
    # c = number_bound_paths(2,1,3,3)
    # d = number_bound_paths(0,0,2,1)
    # print(c * d)
    # print(a * b + c * d)
    # print('---')
    # print('---')
    # a = number_bound_paths(3,1,3,3)
    # b = number_bound_paths(0,0,3,1)
    # print(a * b)
    # c = number_bound_paths(2,2,3,3)
    # d = number_bound_paths(0,0,2,2)
    # print(c * d)
    # print(a * b + c * d)
    # print('---')
    # print('---')























#
