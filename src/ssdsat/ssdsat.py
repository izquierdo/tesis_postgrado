from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE
import os
import logging
import re

import mcdsat.mcd
import mcdsat.rw
import preferences
import options
from qrp.views import View, Predicate, Argument

# Possible SSDSAT targets

def mcd(views, queries, ontology, costs, preflist):
    # generate the MCD theory
    t = mcdsat.mcd.mcd_theory(queries[0], views, ontology)

    # add preferences to the theory
    if preflist:
        pref_t = preferences.preference_clauses(queries[0], views, preflist, t)
    else:
        pref_t = t

    # feed the theory to the d-DNNF compiler
    nnf_filename = compile_ddnnf(pref_t)

    # enumerate the models of the d-DNNF theory
    models = enumerate_models(nnf_filename)

    for m in models:
        print map(lambda v : t.vs.reverse(v), m)

def rw(views, queries, ontology, costs, preflist):
    # generate the MCD theory
    t = mcdsat.mcd.mcd_theory(queries[0], views, ontology)

    # add preferences to the theory
    if preflist:
        pref_t = preferences.preference_clauses(queries[0], views, preflist, t)
    else:
        pref_t = t

    # generate the RW theory based on the MCD theory
    rw_t = mcdsat.rw.rw_theory(queries[0], views, pref_t)

    # feed the theory to the d-DNNF compiler
    nnf_filename = compile_ddnnf(rw_t)

    # enumerate the models of the d-DNNF theory
    models = enumerate_models(nnf_filename)

    #TODO move somewhere more suitable
    if options.logging_output_file:
        modelcount = count_models(nnf_filename)
        ff = open(options.logging_output_file + ".count", "w")
        print >> ff, modelcount
        ff.close()

        esttime = model_enumeration_time(nnf_filename)
        ff = open(options.logging_output_file + ".time", "w")
        print >> ff, esttime
        ff.close()

    for m in models:
        (v, mapping) = rw_rebuild(queries[0], views, rw_t, m)
        print "%s, %s" % (v, ", ".join(["%s=%s" % (a,b) for (a,b) in mapping]))

def bestrw(views, queries, ontology, costs, preflist):
    # generate the MCD theory
    t = mcdsat.mcd.mcd_theory(queries[0], views, ontology)

    # add MCD preferences to the theory
    pref_t = preferences.preference_clauses(queries[0], views, preflist, t)

    # generate the RW theory based on the MCD theory
    rw_t = mcdsat.rw.rw_theory(queries[0], views, pref_t)

    # add RW preferences to the theory
    pref_rw_t = preferences.preference_rw_clauses(queries[0], views, preflist, rw_t)

    # feed the theory to the d-DNNF compiler
    nnf_filename = compile_ddnnf(pref_rw_t)

    # generate the the cost file
    cost_file = preferences.preference_cost_file(preflist if preflist else [], pref_rw_t, len(views))

    # find the best model of the d-DNNF theory and its cost
    (cost, model) = enumerate_best_model(nnf_filename, cost_file)

    #TODO move somewhere more suitable
    if options.logging_output_file:
        modelcount = count_models(nnf_filename)
        ff = open(options.logging_output_file + ".count", "w")
        print >> ff, modelcount
        ff.close()

        esttime = model_enumeration_time(nnf_filename)
        ff = open(options.logging_output_file + ".time", "w")
        print >> ff, esttime
        ff.close()

    print cost, rw_rebuild(queries[0], views, pref_rw_t, model)

# Target-specific supporting methods

def rw_rebuild(query, views, theory, model):
    #TODO complete implementation
    model_views = {}
    model_goals = {}
    model_mappings = {}

    for n in xrange(len(query.body)):
        model_mappings[n] = []

    for v in model:
        var = theory.vs.rev(v)
        copy = var[-1] # the last element marks the copy number
        kind = var[0]

        if kind == 'v':
            model_views[copy] = var[1]
        elif kind == 'g':
            model_goals[copy] = var[1]
        elif kind == 't':
            model_mappings.setdefault(copy, []).append((var[1], var[2]))

    goals = []
    newvar = 0

    for n in xrange(len(query.body)):
        args = []

        for arg in views[model_views[n]-1].head.arguments:
            appended = False

            for (x, y) in model_mappings[n]:
                if arg == y:
                    args.append(x)
                    appended = True
                    break

            if not appended:
                args.append("_" + str(newvar))
                newvar += 1

        if model_views[n] > 0:
            goals.append(Predicate(views[model_views[n]-1].head.name, args))

    mappings = set()

    for n in model_mappings:
        for (a,b) in model_mappings[n]:
            view_name = views[model_views[n]-1].head.name
            nb = Argument("%s_{%s}" % (b.name, view_name), b.constant)
            mappings.add((a,nb))

    return (View(query.head, goals), mappings)

# External tools

def compile_ddnnf(theory):
    """
    Returns the filename of the d-DNNF #TODO better to return file-like object?
    """
    #TODO better to return file-like object?

    logging.info("[Compile to DNNF]")

    if "cnfprefix" in options.user_options:
        selected_cnf_file = open(options.user_options["cnfprefix"] + ".cnf", "w")
    else:
        selected_cnf_file = NamedTemporaryFile(prefix="ssdsat.", suffix=".cnf")

    with selected_cnf_file as cnf_file:
        theory.write_unweighted_cnf(cnf_file)
        cnf_file.seek(0)

        args = [options.c2d,
                "-in", cnf_file.name,
                "-smooth",
                "-reduce",
                "-dt_method", "4"]

        c2d_process = Popen(args, stdout = open(os.devnull, 'r'))
        c2d_process.wait()

        nnf_filename = "{0}.nnf".format(cnf_file.name)

    return nnf_filename

def model_enumeration_time(nnf_filename):
    """
    Count the models of the d-DNNF theory specified at the given file and
    return the number as an integer.
    """

    logging.info("[Calculate model enumeration time]")

    args = [options.models,
            "--write-models",
            "--num", str(options.max_models),
            nnf_filename]

    models_process = Popen(args, stdout = PIPE)
    models_process.wait()

    models = models_process.stdout.readlines()

    model_enum_time_line = models[-1]
    time_str = re.search("^main: total time (.+) seconds$", model_enum_time_line).group(1)

    #TODO deberia outputear cuantos calcule, para hacer la division correctamente
    return float(time_str)

def count_models(nnf_filename):
    """
    Count the models of the d-DNNF theory specified at the given file and
    return the number as an integer.
    """

    logging.info("[Count models]")

    args = [options.models,
            nnf_filename]

    models_process = Popen(args, stdout = PIPE)
    models_process.wait()

    models = models_process.stdout.readlines()

    model_count_line = models[3]
    eln = re.search("#models=([\d+-.e]+) ", model_count_line)
    if eln:
        model_str = eln.group(1)
    else:
        model_str = 2**32

    return int(float(model_str))

def enumerate_models(nnf_filename):
    """
    Enumerate the models of the d-DNNF theory specified at the given file and
    return them in a list. Each model is encoded as a list of the integer IDs
    of the variables made true in it.
    """

    logging.info("[Enumerate models]")

    args = [options.models,
            "--write-models",
            "--num", str(options.max_models),
            nnf_filename]

    models_process = Popen(args, stdout = PIPE)
    models_process.wait()

    models = models_process.stdout.readlines()

    #filter unneeded output
    for (i, e) in enumerate(models):
        if e.strip() == "--- models begin ---":
            begin = i + 1
            break

    for (i, e) in enumerate(reversed(models)):
        if e.strip() == "---- models end ----":
            end = len(models) - i - 1

    cleanup = lambda m : map(int, m.strip().strip("{}").split())
    return map(cleanup, models[begin:end])

def enumerate_best_model(nnf_filename, cost_filename):
    """
    Find a best model of the d-DNNF theory specified at the given file and
    return it in a list if it exists. The model is encoded as a list of the
    integer IDs of the variables made true in it.
    """

    logging.info("[Best model]")

    args = [options.bestmodel,
            "-c", cost_filename,
            nnf_filename]

    models_process = Popen(args, stdout = PIPE)
    models_process.wait()

    models = models_process.stdout.readlines()

    #the output line is the 3rd one
    output = models[2].strip()
    pair = output.split("{")

    cost = int(pair[0])
    bestmodel = map(int, pair[1].strip(" }").strip().split())

    return (cost, bestmodel)
