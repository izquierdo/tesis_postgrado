#!/usr/bin/env python

import getopt
import logging
import sys

import options
import qrp.parsing
import ssdsat

def usage():
    usage_str = "Usage: {program} -t <target> -v <views> -q <query> [-o <ontology>] [-c <costs>] [-p <prefs>]\n"
    usage_str += " where <target> is one of the following: MCD, RW\n"
    usage_str += " and all other parameters are filenames\n"

    print usage_str.format(program = sys.argv[0]),

def get_options(argv):
    try:
        opts, args = getopt.getopt(argv, "hv:q:o:c:p:t:")
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    views = queries = ontology = costs = preferences = target = None

    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt == "-v":
            views = arg
        elif opt == "-q":
            queries = arg
        elif opt == "-o":
            ontology = arg
        elif opt == "-c":
            costs = arg
        elif opt == "-p":
            preferences = arg
        elif opt == "-t":
            target = arg

    if not views or not queries or not target:
        usage()
        sys.exit(1)

    return (target, views, queries, ontology, costs, preferences)

def main(argv):
    logging.basicConfig(level=options.loglevel, format="%(message)s")

    (target, views, queries, ontology, costs, preferences) = get_options(argv[1:])

    with open(views) as viewfile:
        viewlist = qrp.parsing.parse(viewfile)

    with open(queries) as queryfile:
        querylist = qrp.parsing.parse(queryfile)

    targets = {}
    targets["MCD"] = ssdsat.mcd
    targets["RW"] = ssdsat.rw

    try:
        f = targets[target]
    except KeyError:
        usage()
        sys.exit(1)

    f(viewlist, querylist, ontology, costs, preferences)

if __name__ == "__main__":
    main(sys.argv)
