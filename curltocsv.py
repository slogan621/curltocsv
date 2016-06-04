#!/usr/bin/python

import sys
import getopt
import subprocess
import time
import os
import json

# curl -w "@format.txt" -o /dev/null -s http://www2.hm.com/zh_cn/index.html

class CurlToCSV:
    def __init__(self, format, domain, domainfile, outfile, outdir, loop, delay, json):
        self._json = json
        self._format = format
        self._domain = domain
        self._domainfile = domainfile
        self._outfile = outfile
        self._outdir = outdir
        if outdir:
            try:
                os.mkdir(outdir)
            except OSError:
                pass
        self._loop = loop
        self._delay = delay
        self._cmd = ["-w", "@{}", "-o", "/dev/null", "-s", "http://{}/index.html"]

    def test(self):
        domains = []
        outfile = None
        if self._domain:
            domains.append(self._domain)
        elif self._domainfile:
            with open(self._domainfile) as f:
                tmp = f.readlines()
                for x in tmp:
                    domains.append(x.rstrip())
        if self._outfile:
            outfile = open(self._outfile, "w")

        first = True
        for y in domains:
            o = None
            for x in range(self._loop):
                if not first:
                    time.sleep(self._delay)
                first = False
                if not o:
                    if not outfile:
                        p = y.replace("/", "_")
                        if self._json:
                            suffix = "json"
                        else:
                            suffix = "csv"
                        o = open("{}/{}.{}".format(self._outdir, p, suffix), "w") 
                    else:
                        o = outfile
                cmdargs = ["curl"]
                cmdargs.append(self._cmd[0])
                cmdargs.append(self._cmd[1].format(self._format))
                cmdargs.append(self._cmd[2])
                cmdargs.append(self._cmd[3])
                cmdargs.append(self._cmd[4])
                cmdargs.append(self._cmd[5].format(y))
                print("Executing {}".format(cmdargs))
                 
                output = subprocess.Popen(cmdargs, stdout=subprocess.PIPE).communicate()[0]
                output = output.split("\n")
                if not self._json:
                    o.write(y)
                    o.write(",")
                    for i, x in enumerate(output):
                        try:
                            o.write(x.split(":")[1])
                            if i < len(output) - 2:
                                o.write(",")
                        except:
                            pass
                else:
                    out = {}
                    out["domain"] = y
                    for x in output:
                        try:
                            tmp = x.split(":")
                            out[tmp[0].strip()] = tmp[1].strip()  
                        except:
                            pass
                    print out
                    o.write(json.dumps(out))
                o.write("\n")
                o.flush()

def usage(name):
    print("{} [-h] [-j] -f format [-d domain] [-w path] [--domainfile path] [--outdir path] [-n loop] [-s seconds]".format(name))
    print("-f format file containing output format for curl")
    print("-j output JSON, not csv")
    print("-d domain issue test to this domain only, --domainfile ignored")
    print("-w path write all results to file, --outdir ignored")
    print("--domainfile path read list of domains from this file, -d ignored")
    print("--outdir path create a domain.txt file in this directory to hold results. One line per each result. -w ignored")
    print("-n loop run test against each domain loop times")
    print("-s seconds sleep number of seconds between each test") 
    sys.exit(2)

def main(name, argv):
    format = None
    domain = None
    domainfile = None
    outfile = None
    outdir = None
    loop = 1
    delay = 0
    json = False

    try:
        opts, args = getopt.getopt(argv,"hjf:d:w:n:s:",["domainfile=","outdir="])
    except getopt.GetoptError:
        usage(name)
    for opt, arg in opts:
        if opt == '-h':
            usage(name)
        elif opt in ("-d"):
            domain = arg
        elif opt in ("-j"):
            json = True
        elif opt in ("-f"):
            format = arg
        elif opt in ("-w"):
            outfile = arg
        elif opt in ("--domainfile"):
            domainfile = arg
        elif opt in ("--outdir"):
            outdir = arg
        elif opt in ("-n"):
            loop = int(arg)
        elif opt in ("-s"):
            delay = int(arg)
        else:
            usage(name)

    if format == None:
        print("Must specify format file -f")
        usage(name)
    if domain != None and domainfile != None or domain == None and domainfile == None:
        print("Must specify one of -d or --domainfile")
        usage(name)
    if outfile != None and outdir != None or outfile == None and outdir == None:
        print("Must specify one of -w or --outdir")
        usage(name)
        
    x = CurlToCSV(format, domain, domainfile, outfile, outdir, loop, delay, json)
    x.test()

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
