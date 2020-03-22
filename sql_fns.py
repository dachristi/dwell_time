#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import pathlib

import mysql.connector

from datetime import datetime
from datetime import date
from datetime import timedelta

class MySQL(object):
    config_file = 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)

    def __init__(self, cmd):
        self.cmd = cmd

        self.cnx = mysql.connector.connect(user=MySQL.config['mysql']['user'],
                                   password=MySQL.config['mysql']['password'],
                                   host=MySQL.config['mysql']['host'],
                                   database=MySQL.config['mysql']['database'])
        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)

    def query(self, *args):
        if args:
            self.cursor.execute(self.cmd, args)
            results = self.cursor.fetchall()
        else:
            self.cursor.execute(self.cmd)
            results = self.cursor.fetchall()
        return results

    def insert(self, args):
        if args:
            self.cursor.execute(self.cmd, args)
        else:
            self.cursor.execute(self.cmd)
        return None


def stats_directional(date_selected):
    year, month, day  = list(date_selected.split('-'))
    start = date(int(year), int(month), int(day))
    end = start + timedelta(1)
    start = str(start) + ' 00:00:00'
    end = str(end) + ' 00:00:00'
    cmd = '''
            SELECT
            SUM(event)/2 total_visitors,
            SUM(unix_timestamp(ts) * (event-1))/60 total_dwell
            FROM ts_directional
            WHERE ts BETWEEN %s AND %s
            ;
            '''
    sql = MySQL(cmd)
    result = sql.query(start, end)
    sql.cursor.close()
    sql.cnx.close()
    total_visitors = int(result[0]['total_visitors'])
    total_dwell = float(result[0]['total_dwell'])
    avg_dwell = round(total_dwell / total_visitors)
    print('%s customers visited with an average dwell time of %s minutes.' % (total_visitors, avg_dwell))
    return {'total_visitors': total_visitors, 'average_dwell': avg_dwell}


def current_visitors_query(date_selected):
    year, month, day  = list(date_selected.split('-'))
    start = date(int(year), int(month), int(day))
    end = start + timedelta(1)
    start = str(start) + ' 00:00:00'
    end = str(end) + ' 00:00:00'
    cmd = '''
            SELECT
            UNIX_TIMESTAMP(CONVERT_TZ(ts, 'UTC', 'America/Los_Angeles')) ts, current_visitors
            FROM
            ts_directional
            WHERE ts BETWEEN %s AND %s
            ;
            '''
    sql = MySQL(cmd)
    result = sql.query(start, end)
    sql.cursor.close()
    sql.cnx.close()
    data = [[int(item['ts'])*1000, item['current_visitors']] for item in result]
    return data


def current_visitors_query_nondirectional(date_selected, query='expected_m'):
    year, month, day  = list(date_selected.split('-'))
    start = date(int(year), int(month), int(day))
    end = start + timedelta(1)
    start = str(start) + ' 00:00:00'
    end = str(end) + ' 00:00:00'
    cmd = '''
            SELECT
            UNIX_TIMESTAMP(CONVERT_TZ(ts, 'UTC', 'America/Los_Angeles')) ts
            FROM
            ts_directional
            WHERE ts BETWEEN %s AND %s
            ;
            '''
    sql = MySQL(cmd)
    result = sql.query(start, end)
    ts_data = [int(item['ts'])*1000 for item in result]
    n = len(ts_data)/2
    print(n)
    if query == 'expected_m':
        cmd = '''
                SELECT
                expected_m AS m
                FROM
                nondirectional_expected_m
                WHERE n = %s
                ORDER BY ts_index
                ;
                '''
    elif query == 'min_m':
        cmd = '''
                SELECT
                min_m AS m
                FROM
                nondirectional_expected_m
                WHERE n = %s
                ORDER BY ts_index
                ;
                '''
    elif query == 'max_m':
        cmd = '''
                SELECT
                max_m AS m
                FROM
                nondirectional_expected_m
                WHERE n = %s
                ORDER BY ts_index
                ;
                '''
    else:
        cmd = '''
                SELECT
                probable_m AS m
                FROM
                nondirectional_expected_m
                WHERE n = %s
                ORDER BY ts_index
                ;
                '''
    sql = MySQL(cmd)
    result = sql.query(n)
    sql.cursor.close()
    sql.cnx.close()
    expected_m = [float(item['m']) for item in result]
    data = [[item[0], item[1]] for item in zip(ts_data, expected_m)]
    total_visitors = len(expected_m)/2.
    dt_list = []
    dt1 = ts_data[0]
    for i in range(1, len(ts_data)):
        dt2 = ts_data[i]
        dt = dt2 - dt1
        dt_list.append(dt)
        dt1 = dt2
    expected_dwell = sum([item[0] * item[1] for item in zip(expected_m[:-1],dt_list)])
    expected_dwell = round(expected_dwell/60/1000/total_visitors,0)

    sql.cursor.close()
    sql.cnx.close()
    return data, total_visitors, expected_dwell


def store_dwell_times(n, dwell_time_list):
    '''Insert select station data from the json file'''

    cmd = '''
            INSERT INTO dwell_times
            (n, dwell_time)
            VALUES
            (%s,%s);
            '''
    sql = MySQL(cmd)
    for datum in dwell_time_list:
        sql.insert((n, datum))
    sql.cursor.close()
    sql.cnx.commit()
    sql.cnx.close()


def store_poisson_data(n, dwell_time, frequency, poisson):
    '''Insert select station data from the json file'''

    cmd = '''
            INSERT INTO frequencies
            (n, dwell_time, relative_frequency, poisson)
            VALUES
            (%s,%s,%s,%s);
            '''
    sql = MySQL(cmd)
    sql.insert((n, dwell_time, frequency, poisson))
    sql.cursor.close()
    sql.cnx.commit()
    sql.cnx.close()


def query_dwell(poisson):
    '''Query all dwell times for N visitors.'''
    cmd = '''
            SELECT dwell_time, relative_frequency
            FROM frequencies
            WHERE n = 30
            AND poisson = %s
            ;
            '''
    sql = MySQL(cmd)
    result = sql.query(poisson)
    sql.cursor.close()
    sql.cnx.close()
    data = [[float(element['dwell_time']), float(element['relative_frequency'])]
                   for element in result]
    return data


def query_dwell_times(N):
    '''Query all dwell times for N visitors.'''
    cmd1 = '''
            SELECT COUNT(1) path_count
            FROM dwell_times
            WHERE n = %s
            ;
            '''

    cmd2 = '''
            SELECT dwell_time, count(1)/%s probability
            FROM dwell_times
            WHERE n = %s
            GROUP BY 1
            ;
            '''

    sql = MySQL(cmd1)
    path_count = sql.query(N)[0]['path_count']
    sql.cmd = cmd2
    result = sql.query(path_count, N)
    sql.cursor.close()
    sql.cnx.close()
    data = [[float(element['dwell_time']), float(element['probability'])]
                   for element in result]

    return data


def epoch_time_converter(datetime_object):
    total_seconds = (datetime_object - datetime(1970, 1, 1)).total_seconds()
    return int(total_seconds) * 1000
