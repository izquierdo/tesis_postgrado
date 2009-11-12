#!/usr/bin/env python

import sys
import generators.flights

def main():
    if len(sys.argv) < 4:
        usage_and_quit()

    commands = {}
    commands['samecompany'] = generators.flights.samecompany

    viewsfilename = sys.argv[1]
    queryfilename = sys.argv[2]

    command = sys.argv[3]

    generator = commands.get(command)

    if generator is None:
        print_usage()
        sys.exit(1)
    
    query, views = generator(sys.argv[4:])

    viewsfile = open(viewsfilename, 'w')
    viewsfile.writelines([str(v) + '\n' for v in views])
    viewsfile.close()

    queryfile = open(queryfilename, 'w')
    queryfile.write(str(query) + '\n')
    queryfile.close()

def print_usage():
    print "Usage: %s <views_file> <query_file> <command> [command_arguments...]" % (sys.argv[0])

if __name__ == "__main__":
    main()