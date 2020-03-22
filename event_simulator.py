

import math
from random import random
from datetime import datetime
from datetime import date
from datetime import timedelta

from sql_fns import MySQL


def main():
    # Directional
    # d = date(2020,2,1)
    # while d < date.today():
    #     print(d)
    #     year = d.year
    #     month = d.month
    #     day = d.day
    #     open = datetime(year, month, day, 7, 0, 0)
    #     close = datetime(year, month, day, 18, 0, 0)
    #     directional(open, close)
    #     d += timedelta(1)
    #directional(datetime(2020, 2, 29, 7, 0, 0), datetime(2020, 2, 29, 18, 0, 0))
    #stats_directional()
    for n in range(50, 150):
        print(n)
        expected_m_similator(n)


# Non-Directional------------------------------
def expected_m_similator(n):
    for ts_index in range(1, 2*n+1):
        expected_m = valid_points(ts_index, n)
        #store_expected_m(n, ts_index, expected_m)
        store_probable_m(n, ts_index, expected_m)
    return None


def valid_points(ts_index, n):
    '''
    ts_index: timestamp index; 1<=i<=2n
    n: number of people in the store
    '''
    valid_coordinates = []
    range_x = [item for item in range(1, ts_index+1)]
    range_x.sort(reverse=True)
    expected_m = 0
    valid_path_count = number_bound_paths(0,0,n,n)
    m_options = []
    for j in range_x:
        # x = number of entrances; y = number of exits
        x = j
        y = ts_index - x
        if x > n:
            continue
        if y > x:
            break
        if x > n:
            break
        valid_coordinates.append((x,y))
        path_count_a = number_bound_paths(x,y,n,n)
        path_count_b = number_bound_paths(0,0,x,y)
        path_count = (path_count_a * path_count_b) / valid_path_count
        m = x - y
        expected_m += m * path_count
        m_options.append((path_count, m))

        #print((x,y), m, m * path_count, 'patha', path_count_a, path_count_b, path_count)
    m_options.sort()
    return m_options[-1][1]
    return expected_m


def number_bound_paths(a,b,c,d):
    bn1 = c + d - a - b
    bd1  = c - a
    bn2 = c + d - a - b
    bd2 = c - b + 1
    all_path_count = binomial_coefficient(bn1, bd1)
    invalid_path_count = binomial_coefficient(bn2, bd2)
    valid_path_count = all_path_count - invalid_path_count
    return valid_path_count


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
        return value2
    else:
        value = math.factorial(n) / (math.factorial(k) * math.factorial(n-k))
        return value


def stirling(n):
    value = math.sqrt(2 * math.pi * n) * (n / math.e)**n
    return value


def stirling_ln(n):
    #value = math.sqrt(2 * math.pi * n) * (n / math.e)**n
    value = 0.5 * math.log(2 * math.pi * n) + n * math.log(n) - n
    #return math.e**value
    return value


def store_expected_m(n, ts_index, expected_m):

    cmd = '''
            INSERT INTO nondirectional_expected_m
            (n, ts_index, expected_m)
            VALUES
            (%s,%s,%s);
            '''
    sql = MySQL(cmd)
    sql.insert((n, ts_index, expected_m))
    sql.cursor.close()
    sql.cnx.commit()
    sql.cnx.close()
    return None


def store_probable_m(n, ts_index, probable_m):

    cmd = '''
            UPDATE nondirectional_expected_m
            SET probable_m = %s
            WHERE n = %s
            AND ts_index = %s
            ;
            '''
    sql = MySQL(cmd)
    sql.insert((probable_m, n, ts_index))
    sql.cursor.close()
    sql.cnx.commit()
    sql.cnx.close()
    return None


# Directional------------------------------
def directional(open, close):
    '''Insert select station data from the json file'''

    cmd = '''
            INSERT INTO ts_directional
            (ts, event, current_visitors)
            VALUES
            (%s,%s,%s);
            '''

    sql = MySQL(cmd)

    ts_list = []
    ts = open

    m = 1
    seconds = random() * 60 * 30  # 60 seconds * 15 minutes
    ts_list.append(open - timedelta(0,seconds))  # employee enters prior to store opening

    while ts < close:
        seconds = random() * 60 * 30  # 60 seconds * 15 minutes
        ts += timedelta(0,seconds)
        ts_list.append(ts)
    if len(ts_list)%2 != 0:
        seconds = random() * 60 * 30  # 60 seconds * 15 minutes
        ts += timedelta(0,seconds)
        ts_list.append(ts)
    print(len(ts_list))

    events = visit_count_simulator(ts_list)
    for event in events:
         sql.insert(event)

    sql.cursor.close()
    sql.cnx.commit()
    sql.cnx.close()


def visit_count_simulator(ts_list):
    N = len(ts_list)
    n = len(ts_list) / 2
    i = 0
    m = 0
    current_visitors = []
    event_list = []
    for ts in ts_list:
        event = state_change(N, n, m, i)
        if event == 0:
            m += 1
        else:
            m -= 1
        current_visitors.append(m)
        event_list.append(event)
        i += 1

    events = zip(ts_list, event_list, current_visitors)
    # for event in events:
    #     print(event)
    return events


def state_change(N, n, m, i):
    '''
    N: # of events
    n: max number of people
    m: current number of people
    i: event identifier
    '''

    if m == 0:
        return 0
    elif m == n:
        return 2
    elif i == N - 1:
        return 2
    elif m == N - i:
        return 2
    else:
        return int(round(random())) * 2


































if __name__ == '__main__':
    main()
