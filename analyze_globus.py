#!/usr/bin/python

import os
import ast
import time
import argparse
import calendar
import datetime

managed_endpoints = {
    "lbnl#lrc":                "b2e0c23d-6d04-11e5-ba46-22000b92c6ec",
    "ucb#brc":                 "d47068d3-6d04-11e5-ba46-22000b92c6ec",
    "bearstore":               "3e3352d0-115e-11e6-a749-22000bf2d559",
    "lbnl#aresn-dtn":          "b23ee2c6-6d04-11e5-ba46-22000b92c6ec",
    "lbnl@aress-dtn":          "b23ee2dc-6d04-11e5-ba46-22000b92c6ec",
    "lbnl#cgrlvector":         "bafbb649-6d04-11e5-ba46-22000b92c6ec",
    "lbnl#cosmic-dtn":         "d922419a-4c97-11e8-8fd6-0a6d4e044368",
    "LBNL Gdrive Access":      "d0774b60-2549-11e7-bc62-22000b9a448b",
    "lbnl#irdata":             "9674ec8a-6920-11e8-9294-0a6d4e044368",
    "lbnl#metal":              "595ae84c-494f-11e6-8222-22000b97daec",
    "lbnl#oak":                "e4c16f48-6d04-11e5-ba46-22000b92c6ec",
    "lbnl#ares":               "dd1ee755-6d04-11e5-ba46-22000b92c6ec",
    "lbnl#mys3endpoint":       "eb412970-9210-11e5-9982-22000b96db58"
}

def months_in_range(start_time, end_time):
    start_year = start_time.tm_year
    start_month = start_time.tm_mon
    end_year = end_time.tm_year
    end_month = end_time.tm_mon

    months = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == start_year and year != end_year:
                if month >= start_month:
                    month_str = str(year) + "/" + str(month).zfill(2)
                    months.append(month_str)
            elif year == end_year and year != start_year:
                if month <= end_month:
                    month_str = str(year) + "/" + str(month).zfill(2)
                    months.append(month_str)
            elif year == start_year and year == end_year:
                if month >= start_month and month <= end_month:
                    month_str = str(year) + "/" + str(month).zfill(2)
                    months.append(month_str)
            else:
                month_str = str(year) + "/" + str(month).zfill(2)
                months.append(month_str)
    return months

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-time',  action="store", dest="start_time", help="the start of the time period to analyze", required=True)
    parser.add_argument('-e', '--end-time', action="store", dest="end_time", help="the end of the time period to analyze", required=True)
    parser.add_argument('-n', '--endpoint-name', action="store", dest="endpoint_name", help="the endpoint to analyze", required=True)
    parser.add_argument('-u', '--user', action="store", dest="user", help="the user to analyze")
    parser.add_argument('-t', '--target', action="store", dest="target", help="the target to analyze")
    parser.add_argument('-f', '--time-format', action="store", dest="time_format", help="use this custom time format for the start and end times")
    args = parser.parse_args()

    start_time = args.start_time
    end_time = args.end_time
    if args.endpoint_name in managed_endpoints: # endpoint referenced by name
        endpoint_name = managed_endpoints[args.endpoint_name]
    elif args.endpoint_name in managed_endpoints.values(): # endpoint referenced by UUID
        endpoint_name = args.endpoint_name
    else:
        print("ERROR: Endpoint " + args.endpoint_name + " is not in the list of managed endpoints.")
        exit()

    user = args.user
    target = args.target
    if args.time_format == None:
        start_time = time.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = time.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
        time_format = "%Y-%m-%dT%H:%M:%S"
    else:
        time_format = args.time_format
        start_time = time.strptime(start_time, time_format)
        # end_time should be at the end of the given day/month, not the beginning
        if "%d" not in time_format:
            endtime_temp = time.strptime(end_time, time_format)
            end_time = end_time + " " + str(calendar.monthrange(endtime_temp.tm_year, endtime_temp.tm_mon)[1]) + " 23:59:59"
            temp_format = time_format + " %d %H:%M:%S"
            end_time = time.strptime(end_time, temp_format)
        elif "%H" not in time_format:
            end_time = end_time + " 23:59:59"
            temp_format = time_format + " %H:%M:%S"
            end_time = time.strptime(end_time, temp_format)
        else:
            end_time = time.strptime(end_time, time_format)

    #print(start_time)
    #print(end_time)

    start_time_seconds = time.mktime(start_time)
    end_time_seconds = time.mktime(end_time)

    months = months_in_range(start_time, end_time)
    files= []
    for month in months:
        filename = "cache/" + endpoint_name + "/" + month
        if os.path.isfile(filename):
            files.append(filename)

    filtered_sessions = []
    for f in files:
        print("File: " + str(f))
    for data_file in files:
        with open(data_file, "r") as fp:
            fp.seek(0)
            sessions = ast.literal_eval(fp.read().replace('\n', ''))
            for session in sessions:
                is_valid = 1
                if str(session['completion_time']) == "None":
                    continue
                else:
                    session_time = time.strptime(str(session['completion_time']), "%Y-%m-%dT%H:%M:%S+00:00")
                    session_time_seconds = time.mktime(session_time)
                    if session_time_seconds >= start_time_seconds and session_time_seconds <= end_time_seconds:
                        pass
                    else:
                        continue
                if user == None:
                    pass
                else:
                    if user in str(session['owner_string']) or user in str(session['source_local_user']) or user in str(session['destination_local_user']):
                        pass
                    else:
                        continue
                if target == None:
                    pass
                else:
                    if (    target in str(session['destination_endpoint']) or target in str(session['destination_endpoint_display_name']) or
                            target in str(session['destination_endpoint_id']) or target in str(session['source_endpoint']) or
                            target in str(session['source_endpoint_display_name']) or target in str(session['source_endpoint_id'])):
                        pass
                    else:
                        continue
                filtered_sessions.append(session)
    
    print(str(len(filtered_sessions)) + " matching sessions found:")
    for session in filtered_sessions:
        direction = ""
        if endpoint_name == str(session['destination_endpoint_id']):
            direction = "inbound"
        elif endpoint_name == str(session['source_endpoint_id']):
            direction = "outbound"
        else:
            print("Something went wrong. Endpoint ID is in neither src or dst of filtered session.")
            exit()
        print("    " + str(session['source_endpoint']) + " --> " + str(session['destination_endpoint']) + " (" + direction + ")")
        print("        User: " + str(session['owner_string']))
        print("        Request time:    " + str(session['request_time']))
        print("        Completion time: " + str(session['completion_time']))
        print("        Bytes: " + str(session['bytes_transferred']))
        print("        Files: " + str(session['files_transferred']))

if __name__ == "__main__":
    main()
