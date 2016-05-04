#!/usr/bin/python

import os
import time
import subprocess

import chatter

SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp", "bin")
USER = os.path.basename(os.path.expanduser("~"))
PATH = os.path.join("/home", USER, ".ttbp")

LIVE = "http://tilde.town/~"
WWW = os.path.join(PATH, "www")
CONFIG = os.path.join(PATH, "config")
DATA = os.path.join(PATH, "entries")

HEADER = ""
FOOTER = ""
FILES = []

MONTHS = {
        "01":"january",
        "02":"february",
        "03":"march",
        "04":"april",
        "05":"may",
        "06":"june",
        "07":"july",
        "08":"august",
        "09":"september",
        "10":"october",
        "11":"november",
        "12":"december"
    }

def load():
    global HEADER
    global FOOTER

    HEADER = open(os.path.join(CONFIG, "header.txt")).read()
    FOOTER = open(os.path.join(CONFIG, "footer.txt")).read()

    load_files()

def load_files():
    global FILES

    FILES = []
    for filename in os.listdir(DATA):
        filename = os.path.join(DATA, filename)
        if os.path.isfile(filename) and os.path.splitext(filename)[1] == ".txt":
            FILES.append(filename)

    FILES.sort()
    FILES.reverse()

def write(outurl="default.html"):
    outfile = open(os.path.join(WWW, outurl), "w")

    outfile.write("<!--generated by the tilde.town blogging platform on "+time.strftime("%d %B %y")+"\nhttp://tilde.town/~endorphant/ttbp/-->\n\n")

    for line in HEADER:
        outfile.write(line)

    #for line in write_placeholder():
    #    outfile.write(line)

    outfile.write("\n")

    for filename in FILES:
        write_page(filename)
        for line in write_entry(filename):
            outfile.write(line)

        outfile.write("\n")

    for line in FOOTER:
        outfile.write(line)

    outfile.close()

    return os.path.join(LIVE+USER,os.path.basename(os.path.realpath(WWW)),outurl)

def write_page(filename):
    # makes a single permalink page

    outurl = os.path.join(WWW, "".join(parse_date(filename))+".html")
    outfile = open(outurl, "w")

    outfile.write("<!--generated by the tilde.town blogging platform on "+time.strftime("%d %B %y")+"\nhttp://tilde.town/~endorphant/ttbp/-->\n\n")

    for line in HEADER:
        outfile.write(line)

    outfile.write("\n")

    for line in write_entry(filename):
        outfile.write(line)

    outfile.write("\n")

    for line in FOOTER:
        outfile.write(line)

    outfile.close()

    return outurl

def write_entry(filename):
    # dump given file into entry format, return as list of strings

    date = parse_date(filename)

    entry = [
        "\t\t<p><a name=\""+date[0]+date[1]+date[2]+"\"></a><br /><br /></p>\n",
        "\t\t<div class=\"entry\">\n",
        "\t\t\t<h5><a href=\"#"+date[0]+date[1]+date[2]+"\">"+date[2]+"</a> "+MONTHS[date[1]]+" "+date[0]+"</h5>\n",
        "\t\t\t<P>"
    ]

    raw = []
    rawfile = open(os.path.join(DATA, filename), "r")

    for line in rawfile:
        raw.append(line)
    rawfile.close()

    for line in raw:
        entry.append(line+"\t\t\t")
        if line == "\n":
            entry.append("</p>\n\t\t\t<p>")

    entry.append("</p>\n")
    entry.append("\t\t\t<p style=\"font-size:.6em; font-color:#808080; text-align: right;\"><a href=\""+"".join(date)+".html\">permalink</a></p>\n")
    entry.append("\n\t\t</div>\n")

    return entry

def parse_date(file):
    # assuming a filename of YYYYMMDD.txt, returns a list of
    # ['YYYY', 'MM', 'DD']

    rawdate = os.path.splitext(os.path.basename(file))[0]

    date = [rawdate[0:4], rawdate[4:6], rawdate[6:]]

    return date

def meta(entries = FILES):
    # takes a list of filenames and returns:
    # [0] absolute path
    # [1] ctime
    # [2] wc -w
    # [3] timestamp "DD month YYYY at HH:MM"
    # [4] entry date YYYY-MM-DD
    # sorted in reverse date order by [4]

    meta = []

    for filename in FILES:
      ctime = os.path.getctime(filename)
      wc = subprocess.check_output(["wc","-w",filename]).split()[0]
      timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(ctime))
      date = "-".join(parse_date(filename))

      meta.append([filename, ctime, wc, timestamp, date])

    meta.sort(key = lambda filename:filename[4])
    meta.reverse()
    return meta

def test():
    load()
    #for x in FILES:
    #  print(x)

    metaTest = meta()

    for x in metaTest:
      print(x)
