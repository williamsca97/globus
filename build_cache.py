#!/usr/bin/python

from __future__ import print_function

import os
import ast
import time
import datetime

def main():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month_time = first - datetime.timedelta(days=1)
    last_year = last_month_time.strftime("%Y")
    last_month = last_month_time.strftime("%m").zfill(2)
    new_data = {}
    print("Loading file...")
    with open("raw_endpoint_data", "r") as fp: 
        fp.seek(0)
        data = ast.literal_eval(fp.read().replace('\n', ''))
    print("File loaded.")
    for ep, _ in data.iteritems():
        print("Endpoint: " + str(ep))
        new_data[ep] = {}
        for session in data[ep]:
            if session['completion_time'] == None:
                continue
            session_time = time.strptime(str(session['completion_time']), "%Y-%m-%dT%H:%M:%S+00:00")
            if session_time.tm_year not in new_data[ep]:
                new_data[ep][session_time.tm_year] = {}
            if session_time.tm_mon not in new_data[ep][session_time.tm_year]:
                new_data[ep][session_time.tm_year][session_time.tm_mon] = []
            new_data[ep][session_time.tm_year][session_time.tm_mon].append(session)
    for ep, _ in new_data.iteritems():
        for year, _ in new_data[ep].iteritems():
            for month, _ in new_data[ep][year].iteritems():
                filename = "cache/" + ep + "/" + str(year) + "/" + str(month).zfill(2)
                folder2 = "cache/" + ep + "/" + str(year)
                folder1 = "cache/" + ep
                print("Cache file: " + filename)
                if not os.path.exists(folder1):
                    os.makedirs(folder1)
                if not os.path.exists(folder2):
                    os.makedirs(folder2)
                #with open(filename, "w") as f:
                #    f.write(str(new_data[ep][year][month]))
                if str(month).zfill(2) == last_month and str(year) == last_year:
                    print("Month and year match. File will be updated.")
                    with open(filename, "w") as f:
                        f.write(str(new_date[ep][year][month]))
                else:
                    print("Month and year do not match. File will not be updated.")


if __name__ == "__main__":
   main()
