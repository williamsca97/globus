#!/usr/bin/python

import os
import ast
import copy
import pprint
from datetime import datetime

'''nodename = "lbnl#lrc"
all_bytes = 0
all_files = 0
all_xfers = 0
all_users = set()
outbound_bytes = 0
outbound_files = 0
outbound_xfers = 0
outbound_users = set()
inbound_bytes = 0
inbound_files = 0
inbound_xfers = 0
inbound_users = set()'''

def main():
    nodename = "lbnl#lrc"
    all_bytes = 0 
    all_files = 0 
    all_xfers = 0 
    all_users = set()
    outbound_bytes = 0 
    outbound_files = 0 
    outbound_xfers = 0 
    outbound_users = set()
    inbound_bytes = 0 
    inbound_files = 0 
    inbound_xfers = 0 
    inbound_users = set()

    sessions = {}
    with open("raw_endpoint_data", "r") as fp:
        fp.seek(0)
        data = ast.literal_eval(fp.read().replace('\n', ''))
        #for line in fp:
        #    print(line)
    pp = pprint.PrettyPrinter(indent=4)
    # by endpoint pair
    good_endpoint_data = []
    for k, v in data.iteritems():
        endpoint_data = data[k]
        for session in endpoint_data:
            tx_timestamp = datetime.strptime(str(session['completion_time']), "%Y-%m-%dT%H:%M:%S+00:00")
            now_timestamp = datetime.now()
            from_last_month = check_month(tx_timestamp, now_timestamp)
            if from_last_month:
                if str(session['status']) == "SUCCEEDED":
                    good_endpoint_data.append(session)
                    # session passes all our checks, we can now add it to the data
                    here = {}
                    if session['source_endpoint'] not in sessions:
                        sessions[session['source_endpoint']] = {}
                    here = sessions[session['source_endpoint']]
                    if session['destination_endpoint'] not in here:
                        here[session['destination_endpoint']] = {}
                    here = here[session['destination_endpoint']]
                    here[session['task_id']] = {}
                    here = here[session['task_id']]
                    here['user'] = session['owner_string']
                    here['bytes'] = session['bytes_transferred']
                    here['files'] = session['files_transferred']
                    here['date'] = tx_timestamp.month
                    here['type'] = session['type']
                    # add to cumulative totals
                    all_users.add(session['owner_string'])
                    all_bytes += session['bytes_transferred']
                    all_files += session['files_transferred']
                    all_xfers += 1
                    if str(session['source_endpoint']) == nodename: # outbound
                        outbound_users.add(session['owner_string'])
                        outbound_bytes += session['bytes_transferred']
                        outbound_files += session['files_transferred']
                        outbound_xfers += 1
                    elif str(session['destination_endpoint']) == nodename: # inbound
                        inbound_users.add(session['owner_string'])
                        inbound_bytes += session['bytes_transferred']
                        inbound_files += session['files_transferred']
                        inbound_xfers += 1
                        
    totals = {}
    for src, _ in sessions.iteritems():
        for dst, _ in sessions[src].iteritems():
            for task, _ in sessions[src][dst].iteritems():
                task = sessions[src][dst][task]
                if src not in totals:
                    totals[src] = {}
                if dst not in totals[src]:
                    totals[src][dst] = {}
                if task['user'] not in totals[src][dst]:
                    totals[src][dst][task['user']] = {}
                if not totals[src][dst][task['user']]: # is empty
                    totals[src][dst][task['user']]['bytes'] = int(task['bytes'])
                    totals[src][dst][task['user']]['files'] = int(task['files'])
                    totals[src][dst][task['user']]['transfers'] = 1
                else:
                    totals[src][dst][task['user']]['bytes'] += int(task['bytes'])
                    totals[src][dst][task['user']]['files'] += int(task['files'])
                    totals[src][dst][task['user']]['transfers'] += 1
    for src, _ in totals.iteritems():
        for dst, _ in totals[src].iteritems():
            print(str(src) + " --> " + str(dst) + ":")
            for user, _ in totals[src][dst].iteritems():
                print("    User: " + str(user))
                print("        Bytes: " + str(totals[src][dst][user]['bytes']))
                print("        Files: " + str(totals[src][dst][user]['files']))
                print("        Sessions: " + str(totals[src][dst][user]['transfers']))
    # by user
    users = {}
    for session in good_endpoint_data:
        if session['owner_string'] not in users:
            users[session['owner_string']] = {}
        here = users[session['owner_string']]
        if session['source_endpoint'] not in here:
            here[session['source_endpoint']] = {}
        here = here[session['source_endpoint']]
        if session['destination_endpoint'] not in here:
            here[session['destination_endpoint']] = []
        here = here[session['destination_endpoint']]
        txfer = {}
        txfer['bytes'] = session['bytes_transferred']
        txfer['files'] = session['files_transferred']
        here.append(txfer)
    for usr, _ in users.iteritems():
        print("User: " + str(user))
        for src, _ in users[usr].iteritems():
            for dst, _ in users[usr][src].iteritems():
                print("    " + str(src) + " --> " + str(dst) + ":")
                for i, txfer in enumerate(users[usr][src][dst]):
                    print("        Transfer #" + str(i + 1) + ":")
                    print("            Bytes: " + str(txfer['bytes']))
                    print("            Files: " + str(txfer['files']))
    # summary
    print("--------------------------------------------------------------------")
    print("Summary:")
    print("    All transfers:")
    print("        Unique users: " + str(len(all_users)))
    print("        Bytes transferred: " + str(all_bytes))
    print("        Files transferred: " + str(all_files))
    print("        Transfer sessions: " + str(all_xfers))
    print("    Inbound transfers:")
    print("        Unique users: " + str(len(inbound_users)))
    print("        Bytes transferred: " + str(inbound_bytes) + " (" + str(int((float(inbound_bytes) / float(all_bytes)) * 100)) + "%)")
    print("        Files transferred: " + str(inbound_files) + " (" + str(int((float(inbound_files) / float(all_files)) * 100)) + "%)")
    print("        Transfer sessions: " + str(inbound_xfers) + " (" + str(int((float(inbound_xfers) / float(all_xfers)) * 100)) + "%)")
    print("    Outbound transfers:")
    print("        Unique users: " + str(len(outbound_users)))
    print("        Bytes transferred: " + str(outbound_bytes) + " (" + str(int((float(outbound_bytes) / float(all_bytes)) * 100)) + "%)")
    print("        Files transferred: " + str(outbound_files) + " (" + str(int((float(outbound_files) / float(all_files)) * 100)) + "%)")
    print("        Transfer sessions: " + str(outbound_xfers) + " (" + str(int((float(outbound_xfers) / float(all_xfers)) * 100)) + "%)")

def check_month(tx_timestamp, now_timestamp):
    if tx_timestamp.month != 1:
        if tx_timestamp.year == now_timestamp.year and tx_timestamp.month == now_timestamp.month - 1:
            return True
        else:
            return False
    else:
        if tx_timestamp.year == now_timestamp.year - 1 and tx_timestamp.month == 12:
            return True
        else:
            return False

main()
