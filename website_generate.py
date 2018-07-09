#!/usr/bin/python

import os
import ast
import calendar

from datetime import datetime

# DO NOT TOUCH. The program WILL break
import Tkinter as tkinter
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np

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

ROTATION_ANGLE = 90

title = "title"
h1 = "h1"
h2 = "h2"
h3 = "h3"
h4 = "h4"
h5 = "h5"
h6 = "h6"
p = "p"

stylesheet = (
    "td, th { \n"
    "    border: 1px solid black;\n"
    "}\n"
    "table {\n"
    "    border-collapse: collapse;\n"
    "}\n"
    )

def doctype():
    return "<!doctype HTML>\n"

def start_html():
    return "<html>\n"

def end_html():
    return "</html>\n"

def start_head():
    return "<head>\n"

def end_head():
    return "</head>\n"

def start_body():
    return "<body>\n"

def end_body():
    return "</body>\n"

def css_style(style):
    return "<style type=\"text/css\">" + style + "</style>\n"

def tag(t, c, n=0):
    return "<" + t + ">" + c + "</" + t + ">" + ("\n" * n)

def hyperlink(h, c):
    return "<a href=\"" + h + "\">" + c + "</a>"

def comment(c, n=0):
    return "<!-- " + c + "-->" + ("\n" * n)

def img(src, n=0):
    return "<img src=\"" + src + "\" />" + ("\n" * n)

def br(n=1):
    return "<br />" * n

def ln(n=1):
    return "\n" * n

def hr():
    return "<hr />\n"

def brln(n=1):
    return "<br />" + ("\n" * n)

def hrln(n=1):
    return "<hr />" + ("\n" * n)

def start_table():
    return "<table>\n"

def end_table():
    return "</table>\n"

def start_row():
    return "<tr>\n"

def end_row():
    return "</tr>\n"

def header_cell(content):
    return "<th>" + content + "</th>\n"

def table_cell(content):
    return "<td>" + content + "</td>\n"

def header_row(items):
    buf = ""
    buf += start_row()
    for item in items:
        buf += header_cell(str(item))
    buf += end_row()
    return buf

def table_row(items):
    buf = ""
    buf += start_row()
    for item in items:
        buf += table_cell(str(item))
    buf += end_row()
    return buf

def bar_chart_lin(state, data, parameter, category, k=[]):
    # image dir: www/images/endpoint_name/year/month/category_parameter.png
    endpoint = state[0]
    year = state[1]
    month = state[2]
    base_dir = "www/images"
    endpoint_dir = base_dir + "/" + endpoint
    year_dir = endpoint_dir + "/" + year
    month_dir = year_dir + "/" + month
    filename = month_dir + "/" + category + "_" + parameter + ".png"
    imgdirs = [base_dir, endpoint_dir, year_dir, month_dir]
    for imgdir in imgdirs:
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
    htmlfilename = ".." + filename[3:]
    labels = [key for key in sorted(data.keys())]
    sizes = [data[item][parameter] for item in sorted(data)]
    dim = 1
    w = 0.75
    dimw = w / dim
    fig1, ax1 = plt.subplots()
    x = np.arange(len(sizes))
    y = [s for s in sizes]
    b = ax1.bar(x, y, dimw, bottom=0.001)
    ax1.set_xticks(x + dimw / 2)
    ax1.set_xticklabels(labels)
    #ax1.set_xtickangle(90)
    plt.title(parameter)
    plt.xticks(rotation=90)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    buf = ""
    buf += img(htmlfilename)
    return buf

def bar_chart_log(state, data, parameter, category, k=[]):
    # image dir: www/images/endpoint_name/year/month/category_parameter.png
    endpoint = state[0]
    year = state[1]
    month = state[2]
    base_dir = "www/images"
    endpoint_dir = base_dir + "/" + endpoint
    year_dir = endpoint_dir + "/" + year
    month_dir = year_dir + "/" + month
    filename = month_dir + "/" + category + "_" + parameter + ".png"
    imgdirs = [base_dir, endpoint_dir, year_dir, month_dir]
    for imgdir in imgdirs:
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
    htmlfilename = ".." + filename[3:]
    if category == "target":
        labels = [data[item]['target_endpoint_name'] for item in sorted(data)]
    elif category == "transfer path":
        labels = []
        for item in sorted(data):
            label_str = data[item]['target_src_name'] + " --> " + data[item]['target_dst_name']
            labels.append(label_str)
    else:
        labels = [key for key in sorted(data.keys())]
    sizes = [data[item][parameter] for item in sorted(data)]
    dim = 1
    w = 0.75
    dimw = w / dim
    fig1, ax1 = plt.subplots()
    x = np.arange(len(sizes))
    y = [s for s in sizes]
    b = ax1.bar(x, y, dimw, bottom=0.001)
    ax1.set_xticks(x + dimw / 2)
    ax1.set_xticklabels(labels)
    #ax1.set_xscale('symlog')
    ax1.set_yscale('symlog')
    #figsize = plt.rcParams["figure.figsize"]
    #figsize[0] = figsize[0] * (len(sizes) / 31.0)
    #plt.rcParams["figure.figsize"] = figsize
    old_figsize = fig1.get_figwidth()
    new_figsize = old_figsize * (float(len(sizes)) / 31.0) * (5.5 / 3.0)
    fig1.set_figwidth(new_figsize, forward=True)
    plt.title(parameter)
    plt.xticks(rotation=90)
    plt.savefig(filename, bbox_inches="tight")
    fig1.set_figwidth(old_figsize, forward=True)
    plt.close()
    buf = ""
    buf += img(htmlfilename)
    return buf

def pie_chart(state, data, parameter, category, k=[]):
    # image dir: www/images/endpoint_name/year/month/category_parameter.png
    endpoint = state[0]
    year = state[1]
    month = state[2]
    base_dir = "www/images"
    endpoint_dir = base_dir + "/" + endpoint
    year_dir = endpoint_dir + "/" + year
    month_dir = year_dir + "/" + month
    filename = month_dir + "/" + category + "_" + parameter + ".png"
    imgdirs = [base_dir, endpoint_dir, year_dir, month_dir]
    for imgdir in imgdirs:
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
    htmlfilename = ".." + filename[3:]
    labels = [key for key in sorted(data.keys())]
    sizes = []
    for item in sorted(data):
        sizes.append(data[item][parameter])
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis("equal")
    plt.title(parameter)
    plt.savefig(filename, bbox_inches="tight")
    plt.close(fig1)
    buf = ""
    buf += img(htmlfilename)
    return buf

def section_charts(state, data, category, function, xvars=[]):
    buf = ""
    print("BAR")
    buf += function(state, data, "tasks", category, k=xvars)
    print("BAZ")
    buf += function(state, data, "files", category, k=xvars)
    buf += function(state, data, "bytes", category, k=xvars)
    return buf

def main():
    paths = {}
    for k in managed_endpoints.keys():
        dk = k.replace('#', '_').replace('@', '_').replace(' ', '-')
        wdir = "www/" + dk
        if not os.path.exists(wdir):
            os.makedirs(wdir)
        sdir = "cache/" + managed_endpoints[k]
        ssubdirs = []
        if os.path.exists(sdir):
            ssubdirs = [name for name in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, name))]
        #print(ssubdirs)
        for ssubdir in ssubdirs:
            sfiles = os.listdir(sdir + "/"  + ssubdir)
            for sfile in sfiles:
                cache = "cache/" + managed_endpoints[k] + "/" + ssubdir + "/" + sfile
                paths[wdir + "/" + ssubdir + "_" + sfile] = (k, ssubdir, sfile, cache)
    
    all_users = {}
    overwrite = 1
    for k in paths.keys():
        print(k + ": " + str(paths[k]))
        if not os.path.exists(k) or overwrite:
            all_users = summarize_month(k, paths[k][0], paths[k][1], paths[k][2], paths[k][3], all_users)

    for user in sorted(all_users):
        print(user + ":")
        for item in all_users[user]:
            print("    " + item)

def summarize_month(filename, endpoint, year, month, cache, all_users):
    all_tasks = 0
    all_files = 0
    all_bytes = 0
    users = {}
    directions = {}
    targets = {}
    transfer_paths = {}
    request_dates = {}
    completion_dates = {}
    request_hours = {}
    completion_hours = {}
    with open(cache, 'r') as fp:
        data = ast.literal_eval(fp.read().replace('\n', ''))
        for task in data:
            # summary table
            all_tasks += 1
            all_files += task['files_transferred']
            all_bytes += task['bytes_transferred']

            # by user
            #all_users.add(task['owner_string'])
            if task['owner_string'] not in all_users:
                all_users[task['owner_string']] = set()
            path_string = str(task['source_endpoint_display_name']) + " --> " + str(task['destination_endpoint_display_name'])
            all_users[task['owner_string']].add(path_string)

            if task['owner_string'] not in users:
                users[task['owner_string']] = {}
                users[task['owner_string']]['tasks'] = 0
                users[task['owner_string']]['files'] = 0
                users[task['owner_string']]['bytes'] = 0
            users[task['owner_string']]['tasks'] += 1
            users[task['owner_string']]['files'] += task['files_transferred']
            users[task['owner_string']]['bytes'] += task['bytes_transferred']

            # by direction
            uuid = managed_endpoints[endpoint]
            if uuid == task['destination_endpoint_id']:
                direction = "inbound"
            elif uuid == task['source_endpoint_id']:
                direction = "outbound"
            else:
                direction = "unknown"
            if direction not in directions:
                directions[direction] = {}
                directions[direction]['tasks'] = 0
                directions[direction]['files'] = 0
                directions[direction]['bytes'] = 0
            directions[direction]['tasks'] += 1
            directions[direction]['files'] += task['files_transferred']
            directions[direction]['bytes'] += task['bytes_transferred']

            # by target
            if direction == "inbound":
                target = task['source_endpoint_id']
                target_name = task['source_endpoint_display_name']
            elif direction == "outbound":
                target = task['destination_endpoint_id']
                target_name = task['destination_endpoint_display_name']
            else:
                if task['source_endpoint_id'] is not None:
                    target = task['source_endpoint_id']
                    target_name = task['source_endpoint_display_name']
                else:
                    target = task['destination_endpoint_id']
                    target_name = task['destination_endpoint_display_name']
            if target == None:
                target = "unknown"
            if target not in targets:
                targets[target] = {}
                targets[target]['name'] = target_name
                targets[target]['tasks'] = 0
                targets[target]['files'] = 0
                targets[target]['bytes'] = 0
            if targets[target]['name'] == None and target_name is not None:
                targets[target]['name'] = target_name
            targets[target]['tasks'] += 1
            targets[target]['files'] += task['files_transferred']
            targets[target]['bytes'] += task['bytes_transferred']

            # by transfer path
            if task['source_endpoint_id'] is not None and task['destination_endpoint_id'] is not None:
                path_name = task['source_endpoint_id'] + " " + task['destination_endpoint_id']
            elif task['source_endpoint_id'] == None:
                path_name = "unknown " + task['destination_endpoint_id']
            else:
                path_name = task['source_endpoint_id'] + " unknown"
            if path_name not in transfer_paths:
                transfer_paths[path_name] = {}
                transfer_paths[path_name]['readable_src'] = task['source_endpoint_display_name']
                transfer_paths[path_name]['readable_dst'] = task['destination_endpoint_display_name']
                transfer_paths[path_name]['tasks'] = 0
                transfer_paths[path_name]['files'] = 0
                transfer_paths[path_name]['bytes'] = 0
            if transfer_paths[path_name]['readable_src'] == None and task['source_endpoint_display_name'] is not None:
                transfer_paths[path_name]['readable_src'] = task['source_endpoint_display_name']
            if transfer_paths[path_name]['readable_dst'] == None and task['destination_endpoint_display_name'] is not None:
                transfer_paths[path_name]['readable_dst'] = task['destination_endpoint_display_name']
            transfer_paths[path_name]['tasks'] += 1
            transfer_paths[path_name]['files'] += task['files_transferred']
            transfer_paths[path_name]['bytes'] += task['bytes_transferred']

            # by request date
            req_timestamp = datetime.strptime(task['request_time'], "%Y-%m-%dT%H:%M:%S+00:00")
            req_date = str(req_timestamp.year) + " " + str(req_timestamp.month) + " " + str(req_timestamp.day).zfill(2)
            if req_date not in request_dates:
                request_dates[req_date] = {}
                request_dates[req_date]['tasks'] = 0
                request_dates[req_date]['files'] = 0
                request_dates[req_date]['bytes'] = 0
            request_dates[req_date]['tasks'] += 1
            request_dates[req_date]['files'] += task['files_transferred']
            request_dates[req_date]['bytes'] += task['bytes_transferred']

            # by completion date
            cmp_timestamp = datetime.strptime(task['completion_time'], "%Y-%m-%dT%H:%M:%S+00:00")
            cmp_date = str(cmp_timestamp.year) + " " + str(cmp_timestamp.month) + " " + str(cmp_timestamp.day).zfill(2)
            if cmp_date not in completion_dates:
                completion_dates[cmp_date] = {}
                completion_dates[cmp_date]['tasks'] = 0
                completion_dates[cmp_date]['files'] = 0
                completion_dates[cmp_date]['bytes'] = 0
            completion_dates[cmp_date]['tasks'] += 1
            completion_dates[cmp_date]['files'] += task['files_transferred']
            completion_dates[cmp_date]['bytes'] += task['bytes_transferred']

            # by request time
            req_hour = str(req_timestamp.hour).zfill(2)
            if req_hour not in request_hours:
                request_hours[req_hour] = {}
                request_hours[req_hour]['tasks'] = 0
                request_hours[req_hour]['files'] = 0
                request_hours[req_hour]['bytes'] = 0
            request_hours[req_hour]['tasks'] += 1
            request_hours[req_hour]['files'] += task['files_transferred']
            request_hours[req_hour]['bytes'] += task['bytes_transferred']

            # by completion time
            cmp_hour = str(cmp_timestamp.hour).zfill(2)
            if cmp_hour not in completion_hours:
                completion_hours[cmp_hour] = {}
                completion_hours[cmp_hour]['tasks'] = 0
                completion_hours[cmp_hour]['files'] = 0
                completion_hours[cmp_hour]['bytes'] = 0
            completion_hours[cmp_hour]['tasks'] += 1
            completion_hours[cmp_hour]['files'] += task['files_transferred']
            completion_hours[cmp_hour]['bytes'] += task['bytes_transferred']

            # by division/research group

            # by transfer path and division/research group

    state_endpoint = endpoint.replace('#', '_').replace('@', '_').replace(' ', '-')
    state_month = month
    state_year = year
    state = [state_endpoint, state_year, state_month]
    
    buf = ""

    buf += doctype()
    buf += start_html()
    buf += start_head()
    buf += tag(title, "Endpoint Usage Report", 1)
    buf += css_style(stylesheet)
    buf += end_head()
    buf += start_body()

    buf += hyperlink("..", "<-- main menu")
    buf += brln()
    buf += hyperlink("../" + endpoint.replace('#', '_').replace('@', '_').replace(' ', '-'), "<-- " + endpoint + " menu")
    buf += brln()
    summary = calendar.month_name[int(month)] + " " + year + " monthly summary for Globus endpoint \"" + endpoint + "\" (" + managed_endpoints[endpoint] + "):"
    buf += tag(h2, summary)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Overall usage:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Tasks", "Files", "Bytes"])
    buf += table_row([all_tasks, all_files, all_bytes])
    buf += end_table()
    buf += ln(2)
    buf += hrln(2)

    print("HELLO")
    buf += tag(h3, "Usage by unique user:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["User", "Tasks", "Files", "Bytes"])
    for user, userdata in sorted(users.iteritems()):
        buf += table_row([user, userdata['tasks'], userdata['files'], userdata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, users, "user", bar_chart_log)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by direction:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Direction", "Tasks", "Files", "Bytes"])
    for direction, dirdata in sorted(directions.iteritems()):
        buf += table_row([direction, dirdata['tasks'], dirdata['files'], dirdata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, directions, "direction", pie_chart)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by target:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Target", "Tasks", "Files", "Bytes"])
    for target, targetdata in sorted(targets.iteritems()):
        if targetdata['name'] is not None:
            target_endpoint_name = targetdata['name'] + " (" + target + ")"
            target_endpoint_name2 = targetdata['name']
        else:
            target_endpoint_name = target
            target_endpoint_name2 = target
        buf += table_row([target_endpoint_name, targetdata['tasks'], targetdata['files'], targetdata['bytes']])
        targetdata['target_endpoint_name'] = target_endpoint_name2
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, targets, "target", bar_chart_log)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by transfer path:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Transfer Path", "Tasks", "Files", "Bytes"])
    for path, pathdata in sorted(transfer_paths.iteritems()):
        if pathdata['readable_src'] == None:
            readable_src = path.split(' ')[0]
        else:
            readable_src = str(pathdata['readable_src'])
        if pathdata['readable_dst'] == None:
            readable_dst = path.split(' ')[1]
        else:
            readable_dst = str(pathdata['readable_dst'])
        readable_path = readable_src + " --> " + readable_dst
        buf += table_row([readable_path, pathdata['tasks'], pathdata['files'], pathdata['bytes']])
        pathdata['target_src_name'] = readable_src
        pathdata['target_dst_name'] = readable_dst
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, transfer_paths, "transfer path", bar_chart_log)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by request date:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Request date", "Tasks", "Files", "Bytes"])
    for date, datedata in sorted(request_dates.iteritems()):
        readable_date = '-'.join(date.split(' '))
        buf += table_row([readable_date, datedata['tasks'], datedata['files'], datedata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, request_dates, "request date", bar_chart_lin)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by completion date:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Completion date", "Tasks", "Files", "Bytes"])
    for date, datedata in sorted(completion_dates.iteritems()):
        readable_date = '-'.join(date.split(' '))
        buf += table_row([readable_date, datedata['tasks'], datedata['files'], datedata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, completion_dates, "completion date", bar_chart_lin)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by request hour:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Request hour", "Tasks", "Files", "Bytes"])
    for date, datedata in sorted(request_hours.iteritems()):
        readable_date = '-'.join(date.split(' '))
        buf += table_row([readable_date, datedata['tasks'], datedata['files'], datedata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, request_hours, "request hour", bar_chart_lin)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(h3, "Usage by completion hour:")
    buf += ln(2)
    buf += start_table()
    buf += header_row(["Completion hour", "Tasks", "Files", "Bytes"])
    for date, datedata in sorted(completion_hours.iteritems()):
        readable_date = '-'.join(date.split(' '))
        buf += table_row([readable_date, datedata['tasks'], datedata['files'], datedata['bytes']])
    buf += end_table()
    buf += ln(2)
    buf += section_charts(state, completion_hours, "completion hour", bar_chart_lin)
    buf += ln(2)
    buf += hrln(2)

    buf += tag(p, "Copyright &copy; Connor Williams, 2018. All rights reserved.")
    buf += end_body()
    buf += end_html()

    with open(filename, 'w') as fp:
        fp.seek(0)
        fp.write(buf)

    return all_users

if __name__ == "__main__":
    main()
