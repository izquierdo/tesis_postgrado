import getopt

from cStringIO import StringIO#TODO debugging only
import qrp.parsing
import sat.cnf
import mcdsat.mcd
import sys

import ssdsat

#viewf = StringIO("v1(X) :- r1(X),r2(X) v2(X) :- r3(X) v3(X) :- r1(X)")
#views = qrp.parsing.parse(viewf)

#queryf = StringIO("q(X) :- r1(X),r3(x)")
#query = qrp.parsing.parse(queryf)[0]

#t = mcdsat.mcd.mcd_theory(query, views)

#t.write_unweighted_cnf(sys.stdout)

def usage():
    print "usage" # TODO

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
        sys.exit(1)

    return (views, queries, ontology, costs, preferences, target)

def main(argv):
    (views, queries, ontology, costs, preferences, target) = get_options(argv[1:])

    with open(views) as viewfile:
        viewlist = qrp.parsing.parse(viewfile)

    with open(queries) as queryfile:
        querylist = qrp.parsing.parse(queryfile)

    targets = {}
    targets["MCD"] = ssdsat.mcd

    if target == "MCD":
        targets[target](viewlist, querylist, ontology, costs, preferences)
    elif target == "RW":
        pass
    elif target == "BESTRW":
        pass
    elif target == "BIGBESTRW":
        pass
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
